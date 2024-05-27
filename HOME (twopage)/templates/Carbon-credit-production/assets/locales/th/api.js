export default {
	page_title: "API Credentials",
	unit:{
		item:'รายการ'
	},
	stat_title: {
		all: "จำนวน ALIAS ทั้งหมด",
		enable: "พร้อมใช้งาน",
		disable: "ระงับการใช้งาน",
	},
	filter: {
		status: {
			all: "สถานะ",
			draft: "Draft",
			released: "Released",
			terminated: "Terminated",
			temporary_close: "Temporary Closed",
		},
		search: "ค้นหา",
		limit: "แสดง {limit}",
	},
	table: {
		header: {
			alias_name: "ชื่อ",
			email: "อีเมล",
			permission: "สิทธิ์การเข้าถึง",
			status: "สถานะ",
			created_date: "วันที่สร้าง",
			last_used: "เรียกใช้งานล่าสุด",
			tools: "เครื่องมือ",
		},
	},
	create_page: {
		page_title: "สร้าง Credential ใหม่",
		manual: {
			_0: "คู่มือการใช้งาน Credential เบื้องต้น",
			_1: `เมื่อสร้าง Credential API สำเร็จ คุณจะได้รับ Access key และ Secret key`,
			_2: `ระบบ Endpoint จะต้องส่ง Access key และ Secret key เพื่อทำการขอ Authentication และจะได้รับ JWT Token ซึงจะมีอายุ 1 ชั่วโมง`,
			_3: `ระบบ Endpoint จะต้องส่ง Access key และ Secret key เพื่อทำการขอ Authentication และจะได้รับ JWT Token ซึงจะมีอายุ 1 ชั่วโมง`,
		},
		form:{
			alias_name:'ชื่อของระบบที่ขอใช้งานระบบ API',
			full_name:'ชื่อ-นามสกุล',
			email:'อีเมล สำหรับให้ระบบส่งแจ้งเตือนการใช้งาน',
			purpose_description:'วัตถุประสงค์หรือรายละเอียดการใช้งาน API',
			account_number:'หมายเลขบัญชี',
			api_permission:'เลือกสิทธิการเข้าใช้งาน API ที่ต้องการ',

		},
		permissionCheck:{
			all_project_pagination:'ดึงข้อมูลโครงการทั้งหมด',
			all_project_pagination_for_transfer:'ดึงข้อมูลโครงการทั้งหมดสำหรับการโอนเครดิต',
			get_project_by_id:'ดึงข้อมูลโครงการ 1 รายการโดย project_id',
			create_project:'บันทึกข้อมูลโครงการใหม่',
			update_project:'ปรับปรุงข้อมูลโครงการ',
			transfer_credit:'บันทึกข้อมูลการซื้อ-ขาย คาร์บอนเครดิต',
			retirement_credit:'Retirement คาร์บอนเครดิต',
			all_account_number:'ดึงข้อมูลหมายเลขบัญชีทั้งหมด',
			all_credit_wallet:'ดึงข้อมูลเครดิตที่ถือครอง',
			all_credit_transaction:'ดึงข้อมูลการทำธุรกรรมเครดิต',
			user_sync_token:'ขอและตรวจสอบการเชื่อมต่อภายนอก'
		}
	},
	edit_page: {
		page_title: "รายละเอียดข้อมูล Credential",
		manual: {
			_0: "คู่มือการใช้งาน Credential เบื้องต้น",
			_1: `เมื่อสร้าง Credential API สำเร็จ คุณจะได้รับ Access key และ Secret key`,
			_2: `ระบบ Endpoint จะต้องส่ง Access key และ Secret key เพื่อทำการขอ Authentication และจะได้รับ JWT Token ซึงจะมีอายุ 1 ชั่วโมง`,
			_3: `ระบบ Endpoint จะต้องส่ง Access key และ Secret key เพื่อทำการขอ Authentication และจะได้รับ JWT Token ซึงจะมีอายุ 1 ชั่วโมง`,
		},
	},
};
