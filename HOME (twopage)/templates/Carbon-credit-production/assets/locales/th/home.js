export default {
	modal:{
        title:'รหัสยืนยันบัญชี',
        subtitle:'รหัสยืนยันบัญชีใช้สำหรับเชื่อมโยงบัญชีระหว่าง องค์การบริหารจัดการก๊าซเรือนกระจก (TGO) และระบบ ตลาดซื้อขายคาร์บอนเครดิต (FTIX) โดยรหัสจะมีอายุ 1 วัน หากรหัสหมดอายุ คุณสามาถสร้างรหัสผ่าน ใหม่โดยกดปุ่มสร้างรหัสใหม่อีกครั้ง',
        label:{
            token:'รหัส',
        },
        request_statement_title:'ขอ Statement',
        filter:{
            month:'เลือกเดือน',
            language:'ภาษา',
            placeholder:'เริ่มต้น - สิ้นสุด',
            email:'อีเมล'
        }

    },
    account:{
		pending_status:'อยู่ระหว่างรออนุมัติจากเจ้าหน้าที่'
	},
    title:{
        credit_list:'รายการเครดิต',
        transaction_history:'ประวัติการทำธุรกรรม',
        account_number:'หมายเลขบัญชี',

        account_list:'บัญชีเครดิต',
		new_account:'บัญชีเครดิตที่รอยืนยัน'
    },
    table:{
        title:'ตัวอย่างข้อมูล',
        header:{
            datetime:'วันที่/เวลา',
            transferor:'ผู้โอน',
            transferee:'ผู้รับ',
            credit_amount:'จำนวนเครดิต',
            remark:'รายละเอียด/หมายเหตุ'
        }
    },

    form_validation:{
        date:'โปรดระบุเดือน',
        lang:'โปรดระบุภาษาของเอกสาร',
        email:'โปรดระบุอีเมลปลายทาง'
    },
    swal: {
		statement: {
			title: {
				success: "สำเร็จ",
				invalid: "เกิดข้อผิดพลาด",
				error: "ไม่สำเร็จ",
			},
			text: {
				success: "ระบบได้ส่งเอกสารไปที่อีเมลของท่านแล้ว",
                check_email:'กรุณาตรวจสอบตามที่อยู่อีเมลต่อไปนี้ {email}',
				invalid: "กรุณากรอกข้อมูลให้ครบถ้วน ก่อนส่งคำขอ",
				error: "ส่งคำขอไม่สำเร็จ กรุณาลองใหม่อีกครั้ง",
			},
		},
	},

};
