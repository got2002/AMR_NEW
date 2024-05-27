export default {
	page_title: "รายการบัญชีคาร์บอนเครดิต",
	button:{
		remove:'ลบบัญชี'
	},
	statCO2VolumeTitle: {
		all: "บัญชีทั้งหมด",
		organization: "องค์กร/หน่วยงานทั้งหมด",
		approved: "ยืนยันแล้ว",
		pending: "รอการยืนยัน",
	},
	card:{
		attach_files:'เอกสารที่แนบมา ({item})',
	},
	filter: {
		role: {
			all: "บทบาททั้งหมด",
			user: "ผู้ใช้ทั่วไป",
			admin: "แอดมิน",
			moderator: "ผู้ดำเนินการ",
		},
		status: {
			all: "สถานะทั้งหมด",
			pending: "รอการยืนยัน",
			approved: "ยืนยันแล้ว",
		},
		organization: "องค์กร/หน่วยงาน",
		search: "ค้นหา",
		limit: "แสดง {limit}",
		addAccount: "เพิ่มบัญชี",
	},
	table: {
		header: {
			account_id: "หมายเลขบัญชี",
			name: "ชื่อบัญชี",
			credit: "เครดิตรวม",
			tool: "เครื่องมือ",
			accountType: "ประเภทบัญชี",
			createAt: "วันที่ขึ้นทะเบียน",
			number_of_projects: "จำนวนโครงการ",
		},
	},
	accountType:{
		guest:'บุคคลธรรมดา',
		juristic:'นิติบุคคล',
		government:'หน่วยงานรัฐ'
	},
	view: {
		page_title: "รายละเอียดบัญชีเครดิต",
		table_credit_balance: "ยอดเครดิตคงเหลือ",
		year: "ปี",
		quantity: "จำนวน",
		date_and_time: "วันและเวลา",
		detailed: "รายละเอียด",
		transferor: "ผู้โอน",
		transferee: "ผู้รับโอน",
		credit: "จำนวน",
		transaction: "ประวัติการทำธุรกรรมคาร์บอน",
		transfer: "โอน",
		status: "สถานะ",
	},
	create_page: {
		page_title: "สร้างบัญชีเครดิต",
		subtitle: "กรุณากรอกข้อมูลให้ครบถ้วน",
		form: {
			title: "ข้อมูลบัญชีเครดิต",
			firstname: "ชื่อ",
			lastname: "นามสกุล",
			organization: "องค์กร/หน่วยงาน",
			role: "บทบาท",
			email: "อีเมล",
			password: "รหัสผ่าน",
			confirm_password: "ยืนยันรหัสผ่าน",
			permission: "สิทธิ์การเข้าถึงข้อมูล",
			dropdowns: {
				accountTypes: {
					all: "เลือกประเภทบัญชี",
				},
				transactionTypes: {
					all: "เลือกประเภทธุรกรรม",
				},
				email: {
					all: "เลือกอีเมล",
				},
			},
			name: "ชื่อบัญชี",
			accountTypes: "ประเภทบัญชี",
			transactionTypes: "ประเภทธุรกรรม",
		},
	},
	transfer: {
		project_number: "หมายเลขโครงการ",
		project_name: "ชื่อโครงการ",
		please_select_a_project: "โปรดเลือกโครงการ",
		remark: "หมายเหตุ",
		transfer: "โอน",
		Please_select_a_transferee: "โปรดเลือกผู้รับโอน",
		Do_you_want_to_transfer_credit: "คุณต้องการโอนเครดิตใช่ไหม",
		successful_transfer: "โอนสำเร็จ",
		carbon_credit_transfer: "โอนคาร์บอนเครดิต",
	},
};
