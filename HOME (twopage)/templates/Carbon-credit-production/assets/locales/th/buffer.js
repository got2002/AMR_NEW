export default {
    page_title: "รายการข้อมูล Buffer",
	tab:{
		buffer:'รายการป้องกันการสูญเสียเครดิต',
		reversal:'รายการยกเลิกเครดิตที่สูญเสีย'
	},
	table: {
		project_id: "รหัสโครการ",
		project_name: "ชื่อโครงการ",
		vintage: "ปี Vintage",
		buffer: "ป้องกันการสูญเสียเครดิต",
		endDate:'วันที่สิ้นสุด',
		createdAt:'วันที่ยกเลิก',
		tool: "เครื่องมือ",
	},
	modal: {
		title: "การรับรองเครดิต",
		title2: "การยกเลิกเครดิตที่สูญเสีย",
		subtitle: "จำนวน buffer ทั้งหมด {amount} tCO2eq",

		remark: "บันทึกช่วยจำ",
		buffer: "Buffer",
        issue:'จำนวนที่ต้องการรับรอง',
		reversal:'จำนวนที่ต้องการยกเลิก',
        total:'คงเหลือ',

		placeholder_remark: "พิมพ์ข้อความที่นี่...",

		validation: {
			required: "โปรดระบุ",
			specification: "โปรดระบุเปอร์เซ็นต์บัฟเฟอร์ที่จะรับรองคาร์บอน",
			specification2: "โปรดระบุเปอร์เซ็นต์บัฟเฟอร์ที่ต้องการยกเลิก",
		},
	},
};
