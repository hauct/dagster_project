from dagster import (
    RunRequest,  # Đối tượng yêu cầu chạy một job
    SensorEvaluationContext,  # Ngữ cảnh đánh giá của sensor
    SensorResult,  # Kết quả của sensor
    sensor  # Decorator để định nghĩa một sensor
)

import os  # Thư viện để làm việc với hệ thống tệp
import json  # Thư viện để làm việc với dữ liệu JSON

from ..jobs import adhoc_request_job  # Import job cần chạy khi sensor kích hoạt

# Định nghĩa một sensor với decorator @sensor
@sensor(
    job=adhoc_request_job  # Sensor này sẽ kích hoạt job 'adhoc_request_job'
)
def adhoc_request_sensor(context: SensorEvaluationContext):
    # Đường dẫn tới thư mục chứa các file yêu cầu
    PATH_TO_REQUESTS = os.path.join(os.path.dirname(__file__), "../../", "data/requests")

    # Lấy trạng thái trước đó từ cursor, nếu không có thì gán là {}
    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}  # Trạng thái hiện tại của các file
    runs_to_request = []  # Danh sách các yêu cầu chạy job

    # Duyệt qua tất cả các file trong thư mục PATH_TO_REQUESTS
    for filename in os.listdir(PATH_TO_REQUESTS):
        file_path = os.path.join(PATH_TO_REQUESTS, filename)
        if filename.endswith(".json") and os.path.isfile(file_path):
            last_modified = os.path.getmtime(file_path)  # Lấy thời gian chỉnh sửa cuối cùng của file

            current_state[filename] = last_modified  # Cập nhật trạng thái hiện tại

            # Nếu file mới hoặc đã được chỉnh sửa từ lần chạy trước, thêm vào danh sách yêu cầu chạy job
            if filename not in previous_state or previous_state[filename] != last_modified:
                with open(file_path, "r") as f:
                    request_config = json.load(f)  # Đọc nội dung file JSON

                    runs_to_request.append(RunRequest(
                        run_key=f"adhoc_request_{filename}_{last_modified}",  # Khóa duy nhất cho yêu cầu chạy
                        run_config={
                            "ops": {
                                "adhoc_request": {
                                    "config": {
                                        "filename": filename,  # Tên file
                                        **request_config  # Nội dung cấu hình từ file JSON
                                    }
                                }
                            }
                        }
                    ))

    # Trả về kết quả của sensor với danh sách các yêu cầu chạy và trạng thái hiện tại dưới dạng JSON
    return SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_state)
    )