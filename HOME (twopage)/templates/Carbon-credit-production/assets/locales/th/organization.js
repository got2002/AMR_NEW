export default {
	page_title: "องค์กร/หน่วยงาน",
	button: {
		remove: "ลบบัญชี",
	},

	filter: {
		organization: "องค์กร/หน่วยงาน",
		search: "ค้นหา",
		limit: "แสดง {limit}",
		addAccount: "เพิ่มบัญชี",
	},
	table: {
		header: {
			organization_name: "ชื่อองค์กร/หน่วยงาน",
			organization_number: "หมายเลของค์กร",
			organization_type: "ประเภท",
			member: "จำนวนสมาชิก",
			tool: "เครื่องมือ",
			no: "ลำดับที่",
		},
	},

	create: {
		page_title: "เพิ่มองค์กร/หน่วยงาน",

		form: {
			organization_name: {
				th: "ชื่อองค์กร/หน่วยงาน (ไทย)",
				en: "ชื่อองค์กร/หน่วยงาน (อังกฤษ)",
			},
			fieldOfIndustry: "ประเภท",
			fieldOfIndustryCustom: "รายละเอียดเพิ่มเติม",
			address: {
				th:'ที่อยู่ (ไทย)',
				en:'ที่อยู่ (อังกฤษ)'
			},
			
			province: "จังหวัด",
			district: "อำเภอ",
			subDistrict: "ตำบล",
			postCode: "หมายเลขไปรษณีย์",
			phone: "หมายเลขโทรศัพท์",
			companyLogo: "สัญลักษณ์องค์กร",
			road: "ถนน",
			website: "เว็บไซต์",
			landArray: "แยก/พื้นที่/ซอย/อื่นๆ",
			fax: "แฟ็กซ์",
			village: "หมู่",
			organization_type:'ประเภทองค์กร',
			juristic:'นิติบุคคล',
			government:'หน่วยงานรัฐ/รัฐวิสาหกิจ',
		},
		form_validation: {
			organization_name: {
				th: "กรุณาระบุชื่อภาษาไทยขององค์กร/หน่วยงาน",
				en: "กรุณาระบุชื่อภาษาอังกฤษขององค์กร/หน่วยงาน",
			},
			type:"กรุณาระบุประเภทขององค์กร/หน่วยงาน",
			type_other:'กรุณาระบุรายละเอียดเพิ่มเติม',
			address: {
				th: "กรุณาระบุที่อยู่ภาษาไทยขององค์กร/หน่วยงาน",
				en: "กรุณาระบุที่อยู่ภาษาอังกฤษขององค์กร/หน่วยงาน",
			},
			province:'กรุณาระบุจังหวัด',
			district:'กรุณาระบุอำเภอ',
			subdistrict:'กรุณาระบุตำบล',
			postCode:'กรุณาระบุหมายเลขไปรษณีย์',
			phone:'กรุณาระบุหมายเลขโทรศัพท์',
			organization_type:'กรุณาระบุประเภทองค์กร'
		},
	},
};
