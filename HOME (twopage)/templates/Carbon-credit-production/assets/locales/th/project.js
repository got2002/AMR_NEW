export default {
    page_title: "ตารางโครงการคาร์บอนเครดิต",
    statCO2VolumeTitle: {
        allProject: "โครงการทั้งหมด",
        verify: "โครงการที่รับรองเครดิตแล้ว",
        pending: "โครงการที่รอการรับรองเครดิต",
        concluded: "สิ้นสุดโครงการ",
    },

    table: {
        title: "",
        header: {
            project_id: "รหัส",
            project_title: "ชื่อโครงการ",
            project_type: "ประเภท",
            project_owner: "เจ้าของโครงการ",
            external_assessors: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ",

            standard: "มาตรฐาน",
            co2_amount: "ปริมาณคาร์บอนเครดิต",
            co2_reduced: "ปริมาณการลด CO2	",
            registered: "วันที่ขึ้นทะเบียน",
            credit_period_project: "ระยะเวลาคิดเครดิตของโครงการ",
            status: "สถานะโครงการ",
            sub_status: "สถานะเครดิต",
            permit_valid_since: "วันที่เริ่มใบอนุญาต",
            no: "ลำดับ",
            lat: "ละติจูด",
            lon: "ลองจิจูด",
            location: "ที่ตั้ง",
            expected: "ประมาณคาดการณ์",
            credit: "ปริมาณคาร์บอนเครดิต",
            serial_number: "Serial Number",
            total_block: "จำนวนเครดิต",
            reason: "จุดประสงค์การยกเลิก",
            "Cooperative Approach": "Cooperative Approach",
            transaction_date: "วันที่ธุรกรรม"
        },
        status: {
            registered: "ขึ้นทะเบียน",

            rejected: "ยกเลิก",
            expired: "สิ้นสุดโครงการ",
        },
        filter: {
            status: {
                all: "สถานะทั้งหมด",
                registered: "ขึ้นทะเบียน",
                rejected: "ยกเลิก",
                expired: "สิ้นสุดโครงการ",

                pending: "รอการรับรอง",
                certificated: "รับรองแล้ว",
            },
            external_assessors: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ",
            type: "ทุกประเภท",
            province: "ทุกจังหวัด",
            co2Min: "ต่ำสุด",
            co2Max: "สูงสุด",
            search: "ค้นหา",
            type_to_search: "พิมพ์เพื่อค้นหา",

            limit: "แสดง {limit}",
            saperate: "ถึง",
            all_standard: "มาตรฐานทั้งหมด",
            all: 'ทั้งหมด',

            label: {
                status: "สถานะโครงการ",
                sub_status: "สถานะเครดิต",
                standard: "มาตรฐาน",
                type: "ประเภท",
                carbon_credit_amount: "ปริมาณคาร์บอนเครดิต",
                crediting_peroid: "ระยะเวลาคิดเครดิตโครการ",
                external_assessors: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ",
                corsia: 'Authorized Use',
                block_range: "หมายเลขเครดิต",
                cancellation_reason_types: "จุดประสงค์การยกเลิก",
                "Cooperative Approach": "Cooperative Approach",
                transaction_date: "วันที่ธุรกรรม",
                vintage_year: "ปีที่ออกเครดิต",
            },
        },
    },
    view_page: {
        programid: "หมายเลขโปรแกรม",
        authorizeduse: "Authorized Use",
        page_title: "รายละเอียดโครงการ",
        project_overview: "รายละเอียดโครงการ",
        project_overview_lang: {
            th: "รายละเอียดโครงการ (ไทย)",
            en: "รายละเอียดโครงการ (อังกฤษ)",
        },
        project_id: "รหัสโครงการ",
        project_type: "ประเภท",
        knp_rule: "ประเภทตาม CCMGM",
        project_owner: "เจ้าของโครงการ",
        project_developer: "ผู้พัฒนาโครงการ",
        project_owner_lang: {
            th: "เจ้าของโครงการ (ไทย)",
            en: "เจ้าของโครงการ (อังกฤษ)",
        },
        project_developer_lang: {
            th: "ผู้พัฒนาโครงการ (ไทย)",
            en: "ผู้พัฒนาโครงการ (อังกฤษ)",
        },
        external_assessors: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ",
        external_assessors_lang: {
            th: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ (ไทย)",
            en: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ (อังกฤษ)",
        },
        registered_date: "วันที่ขึ้นทะเบียนโครงการ",
        credit_period_project: "ระยะเวลาคิดเครดิตของโครงการ",
        standard: "มาตรฐาน",
        project_images: "รูปภาพโครงการ",

        registered_doc: "เอกสารขึ้นทะเบียนโครงการ",
        additional_doc: "เอกสารอื่นๆเพิ่มเติม",

        filename: "ชื่อไฟล์",
        file_type: "ประเภทไฟล์",
        project_status: "สถานะโครงการ",
        cancelled: "ยกเลิกโครงการ",
        expired: "สิ้นสุดโครงการ",
        registered: "ขึ้นทะเบียนแล้ว",
        adress_position_title: "รายการตำแหน่งทั้งหมดในโครงการ ({amount} ตำแหน่ง)",
        estimated_greenhouse_gases_reduction: "ปริมาณก๊าซเรือนกระจกที่คาดว่าจะลด/กักเก็บได้ (tCO<sub>2</sub>eq/year)",
        approved_carbon_credits: "ปริมาณคาร์บอนเครดิตที่ได้รับการรับรอง (tCO<sub>2</sub>eq)",
        carbon_credits_verified_table: "ตารางการรับรองคาร์บอนเครดิต",
        credit_period: "ระยะเวลาคิดเครดิต",
        greenhouse_gases_amount_approve: "การรับรองปริมาณก๊าซเรือนกระจก",
        status_certificate_carbon: "สถานะ",

        certicate_carbon: {
            certified_carbon_credit: "คาร์บอนเครดิตที่ได้รับการรับรอง",
            document: "เอกสาร",
            status: "สถานะ",
            quantity: "ปริมาณ",
            issuance_date:'วันที่ออกเครดิต',
            cancellation:'การยกเลิกเครดิต',
            percent_buffer:'ป้องกันการสูญเสียเครดิต',
        },
        total: "รวม",
        co_benefit: "ผลประโยชน์ร่วม",
        co_benefit_lang: {
            th: "ผลประโยชน์ร่วม (ไทย)",
            en: "ผลประโยชน์ร่วม (อังกฤษ)",
        },
        environmental: "ด้านสิ่งแวดล้อม",
        societal: "ด้านสังคม",
        economical: "ด้านเศรษฐกิจ",
        latitude: "ละติจูด",
        longitude: "ลองจิจูด",
        ton: "ตัน",
        pending_approval: "รอการอนุมัติ",
        sum: "รวม",
        Click_to_select_a_file: "คลิกเพื่อเลือกไฟล์",
        or_drag: "หรือลากไฟล์ลงที่นี่",
        amount: "จำนวน",
        message_to_user: "ข้อความถึงผู้ใช้",
        start_date: "วันที่เริ่ม",
        end_date: "วันที่สิ้นสุด",
        vintage_start: "ปีที่เริ่ม",
        vintage_end: "ปีที่สิ้นสุด",
        account:'บัญชี',
        reference_link:'อ้างอิง'
    },
    create_page: {
        programid: "หมายเลขโปรแกรม",
        authorizeduse: "Authorized Use",
        page_title: "เพิ่มโครงการคาร์บอนเครดิต",
        dropdowns: {
            project_type: "เลือกประเภทโครงการ",
            project_type_ccmgm: "เลือกประเภทโครงการ CCMGM",
        },
        project_type: "ประเภท",
        project_id: "รหัสโครงการ",
        project_name: {
            th: "ชื่อโครงการ (ไทย)",
            en: "ชื่อโครงการ (อังกฤษ)",
        },
        knp_rule: "ประเภทตาม CCMGM",
        standard: "มาตรฐาน",

        project_owner: "เจ้าของโครงการ",
        project_developer: "ผู้พัฒนาโครงการ",
        project_owner_lang: {
            th: "เจ้าของโครงการ (ไทย)",
            en: "เจ้าของโครงการ (อังกฤษ)",
        },
        project_developer_lang: {
            th: "ผู้พัฒนาโครงการ (ไทย)",
            en: "ผู้พัฒนาโครงการ (อังกฤษ)",
        },
        external_assessors: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ",
        external_assessors_lang: {
            th: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ (ไทย)",
            en: "ผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ (อังกฤษ)",
        },
        registered_date: "วันที่ขึ้นทะเบียนโครงการ",
        credit_period_project: "ระยะเวลาคิดเครดิตของโครงการ",
        project_investment: "เงินลงทุนโครงการ (ล้านบาท)",
        project_images: "รูปภาพโครงการ",

        reduction_methods: {
            title: "ระเบียบวิธีลดก๊าซเรือนกระจกที่ใช้",
            name: "ชื่อเอกสาร",
            document_version: "เวอร์ชั่นเอกสาร",
            description: "คำอธิบายเพิ่มเติม",
        },
        address: {
            title: "ที่อยู่โครงการ",
            subtitle: "ที่อยู่",
            subtitle_lang: {
                th: "ที่อยู่ (ไทย)",
                en: "ที่อยู่ (อังกฤษ)",
            },
        },

        registered_doc: "เอกสารขึ้นทะเบียนโครงการ",
        additional_doc: "เอกสารอื่นๆเพิ่มเติม",

        filename: "ชื่อไฟล์",
        file_type: "ประเภทไฟล์",
        project_status: "สถานะโครงการ",
        estimated_greenhouse_gases_reduction: "ปริมาณก๊าซเรือนกระจกที่คาดว่าจะลด/กักเก็บได้ (tCO<sub>2</sub>eq/year)",
        approved_carbon_credits: "ปริมาณคาร์บอนเครดิตที่ได้รับการรับรอง (tCO<sub>2</sub>eq)",
        carbon_credits_verified_table: "ตารางการรับรองคาร์บอนเครดิต",
        credit_period: "ระยะเวลาคิดเครดิต",
        greenhouse_gases_amount_approve: "การรับรองปริมาณก๊าซเรือนกระจก",
        total: "รวม",
        co_benefit: "ผลประโยชน์ร่วม",
        environmental: "ด้านสิ่งแวดล้อม",
        societal: "ด้านสังคม",
        economical: "ด้านเศรษฐกิจ",
        latitude: "ละติจูด",
        longitude: "ลองจิจูด",
        ton: "ตัน",
        pending_approval: "รอการอนุมัติ",
        sum: "รวม",
        Click_to_select_a_file: "คลิกเพื่อเลือกไฟล์",
        or_drag: "หรือลากไฟล์ลงที่นี่",
        amount: "จำนวน",
        message_to_user: "ข้อความถึงผู้ใช้",
        start_date: "วันที่เริ่ม",
        end_date: "วันที่สิ้นสุด",
        vintage_year: 'ปี',

        form_validation: {
            project_name: "กรุณาระบุชื่อโครงการ",

            address: "กรุณาระบุที่อยู่โครงการ",
            project_type: "กรุณาระบุประเภทโครงการ",
            knp_rule: "กรุณาระบุประเภทตาม CCMGM",
            project_owner: "กรุณาระบุเจ้าของโครงการ",
            external_assessors: "กรุณาระบุผู้ประเมินภายนอกสำหรับโครงการภาคสมัครใจ",
            project_developer: "กรุณาระบุผู้พัฒนาโครงการ",
            registered_date: "กรุณาระบุวันที่ขึ้นทะเบียนโครงการ",
            credit_period_project: "กรุณาระบุระยะเวลาคิดเครดิตของโครงการ",
            project_investment: "กรุณาระบุเงินลงทุนโครงการ",
            standard: "กรุณาระบุมาตรฐานของโครงการ",

            reduction_methods: {
                name: "กรุณาระบุชื่อเอกสาร",
            },

            estimated_greenhouse_gases_reduction: "กรุณาระบุปริมาณก๊าซเรือนกระจกที่คาดว่าจะลด/กักเก็บได้ (tCO<sub>2</sub>eq/year)",

            latitude: "กรุณาระบุพิกัดละติจูด",
            longitude: "กรุณาระบุพิกัดลองติจูด",
            project_type_by_extens: "",
            project_activity: "กรุณาระบุรายละเอียดโครการ",

            certificated_carbon_credit: {
                certification_date: "กรุณาระบุวันที่คิดเครดิต",
                start_date: "กรุณาระบุวันที่เริ่มต้นการคิดเครดิต",
                end_date: "กรุณาระบุวันที่สิ้นสุดการคิดเครดิต",
                credit: "กรุณาระบุจำนวนเครดิต",
                file: "กรุณาระบุไฟล์เอกสารการรับรองคาร์บอนเครดิต",
            },
            programid: "กรุณาระบุหมายเลขโปรแกรม",
            authorizeduse: "กรุณาระบุ Authorized Use",
        },
    },
};