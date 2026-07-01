from io import BytesIO

from openpyxl import Workbook


class ExcelExportService:
    def credentials_sheet(
        self,
        users,
    ):
        wb = Workbook()

        ws = wb.active

        ws.append(
            [
                "Name",
                "Username",
                "Password",
            ]
        )

        for user in users:
            ws.append(
                [
                    user["name"],
                    user["username"],
                    user["password"],
                ]
            )

        stream = BytesIO()

        wb.save(stream)

        stream.seek(0)

        return stream


excel_export_service = ExcelExportService()
