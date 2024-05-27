export default {
	page_title: "ธุรกรรมการโอนเครดิต",
	
	setting:{
		auto_approve:'การอนุมัติแบบอัตโนมัติ'
	},
	filter: {
		role: {
			all: "บทบาททั้งหมด",
			user: "ผู้ใช้ทั่วไป",
			admin: "แอดมิน",
			moderator: "ผู้ดำเนินการ",
		},
		status: {
			pending: "รออนุมัติ",
			approved: "อนุมัติแล้ว",
			all: "สถานะทั้งหมด",
		},
		organization: "องค์กร/หน่วยงาน",
		search: "ค้นหา",
		limit: "แสดง {limit}",

	},
	table: {
		header: {
			project_id: "รหัสโครงการ",
			project_title: "ชื่อโครงการ",
			sender:'ผู้โอนคาร์บอนเครดิต',
			receiver:'ผู้รับคาร์บอนเครดิต',
			amount:'ยอดโอน',
			status:'สถานะ',
			date:'วันที่ดำเนินการ',
			no:'ลำดับที่'
		},
	},
	transfer: {
		project_number: "Project number",
		project_name: "Project name",
		please_select_a_project: "Please select a project",
		remark: "Remark",
		transfer: "Transfer",
		Please_select_a_transferee: "Please select a transferee",
		Do_you_want_to_transfer_credit: "Do you want to transfer credit",
		successful_transfer: "Successful transfer",
		carbon_credit_transfer: "Carbon credit transfer",
	},
};
