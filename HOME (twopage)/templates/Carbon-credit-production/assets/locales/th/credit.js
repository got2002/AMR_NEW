export default {
    page_title: "บริหารรายการเครดิต",
    min: 'น้อยสุด',
    max: 'มากสุด',
    table: {
        title: "",
        header: {
            project_id: "รหัสโครการ",
            project_title: "ชื่อโครงการ",
            vintage_year: "ปี Vintage",
            start_block: "บล็อคเริ่มต้น",
            block: "บล็อค",
            end_block: "บล็อคสิ้นสุด",
            credit_amount: "จำนวนเครดิต",
            lastest_update: "ปรับปรุงข้อมูลล่าสุด",
        },
    },
    modal: {
        title: 'โอนคาร์บอนเครดิต',
        subtitle: 'จำนวนคาร์บอนเครดิตทั้งหมด {amount} เครดิต',
        transaction_type: 'ประเภทการทำธุรกรรม',
        receiver_account: 'บัญชีผู้รับโอน',
        remark: 'บันทึกช่วยจำ',
        amount: 'จำนวนเครดิต',

        placeholder_remark: 'พิมพ์บันทึกของคุณ...',
        price: 'ราคาขาย',

        add_reason: 'ระบุเหตุผล',
        specification: 'โปรดเลือกเหตุผล',
        offset_emissions: 'การชดเชยการปล่อยก๊าซคาร์บอนเรือนกระจก',
        result_base_payment: 'ผลตอบแทนตามผลลัพธ์',
        other_purpose: 'เหตุผลอื่นๆ',
        specify_further: 'ระบุเพิ่มเติม',
        on_behalf_of: 'ในนามของ',
        email: 'อีเมล',

        registered: "อยู่ในระบบ",
        non_registered: "ไม่อยู่ในระบบ",

        validation: {
            transaction_type: 'กรุณาระบุประเภทการทำธุรกรรม',
            receiver_account: 'กรุณาระบุบัญชีผู้รับโอน',
            invalid_credit: 'จำนวนเครดิตไม่ถูกต้อง',
            invalid_price: 'ราคาขายไม่ถูกต้อง',
            invalid_email: 'รูปแบบอีเมลไม่ถูกต้อง',

            required: 'โปรดระบุ',


        }

    }
};