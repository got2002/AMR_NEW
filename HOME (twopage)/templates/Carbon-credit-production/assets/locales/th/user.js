export default {
    role: {
        admin: "แอดมิน",
        registrar: "นายทะเบียน",
        user: " ผู้ใช้งานทั่วไป",
    },
    page_title: "ตารางบัญชีผู้ใช้งาน",
    statCO2VolumeTitle: {
        all: "บัญชีทั้งหมด",
        organization: "องค์กร/หน่วยงานทั้งหมด",
        approved: "ยืนยันแล้ว",
        rejected: "ปฏิเสธแล้ว",
        pending: "รอการยืนยัน",
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
    },
    table: {
        header: {
            user_id: "ลำดับบัญชี",
            name: "ชื่อ",
            email: "อีเมล",
            organization: "องค์กร/หน่วยงาน",
            role: "บทบาท",
            status: "สถานะ",
            registere_date: "วันที่ขึ้นทะเบียน",
            last_login: "เข้าสู่ระบบล่าสุด",
            tool: "เครื่องมือ",
        },
    },
    view: {
        page_title: "รายละเอียดข้อมูลผู้ใช้งาน",
        approve_page_title: "รายละเอียดคำร้อง",

        form: {
            profile_title: 'ข้อมูลทั่วไป',
            account_title: 'ข้อมูลบัญชีเครดิต',
            document: 'เอกสารแนบ',
            part: 'ส่วนที่ {number}'
        }
    },
    create_page: {
        page_title: "สร้างบัญชีผู้ใช้",
        subtitle: "กรุณากรอกข้อมูลให้ครบถ้วน",
        form: {
            title: "ข้อมูลส่วนตัว",
            firstname: "ชื่อ",
            lastname: "นามสกุล",
            organization: "องค์กร/หน่วยงาน",
            role: "บทบาท",
            email: "อีเมล",
            password: "รหัสผ่าน",
            confirm_password: "ยืนยันรหัสผ่าน",
            permission: "สิทธิ์การเข้าถึงข้อมูล",
            dropdowns: {
                organization: {
                    all: "เลือกองค์กร/หน่วยงาน",
                },
                role: {
                    all: "เลือกบทบาท",
                },
            },
            account_type: "ประเภทบัญชี",
        },
    },
    change_password_tab: "รหัสผ่าน",
    change_password_sent_mail_option: "สร้างและส่งรหัสผ่านไปยังอีเมลอัตโนมัติ",
    change_password_sent_mail_message: "ระบบจะทำการสุ่มรหัสผ่านและส่งรหัสผ่านใหม่ไปที่อีเมล <span class='font-bold'>{email}</span> หลังจากดำเนินการแล้ว ระบบจะทำการเปลี่ยนรหัสผ่านทันที โปรดตรวจสอบความถูกต้องของอีเมลก่อนดำเนินการทุกครั้ง",
    change_password_sent_mail_option_button: "ส่งรหัสผ่าน",
    change_password_typing_option: "กําหนดรหัสผ่านเอง",

};