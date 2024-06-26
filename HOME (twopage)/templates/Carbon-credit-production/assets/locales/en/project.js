export default {
    page_title: "Carbon Credit Project Inventory",
    statCO2VolumeTitle: {
        allProject: "All Projects",
        verify: "Certified",
        pending: "Pending Certification",
        concluded: "Projects Ended",
    },

    table: {
        title: "",
        header: {
            project_id: "Project ID",
            project_title: "Project Title",
            project_type: "Project Type",
            project_owner: "Project Owner",
            standard: "Standard",
            co2_amount: "Carbon Credits",
            co2_reduced: "CO2 Reduced",
            registered: "Registration Date",
            status: "Project Status",
            sub_status: "Credit Status",
            credit_period_project: "Crediting Period",
            external_assessors: "Validation/Verification Body",

            permit_valid_since: "Permit valid since",
            no: "No.",
            lat: "Lat",
            lon: "Lon",
            location: "Location",
            expected: "Expected",
            credit: "Carbon Credits Issued",
            serial_number: "Serial Number",
            total_block: "Quantity",
            reason: "Cancellation Purpose",
            "Cooperative Approach": "Cooperative Approach",
            transaction_date: "Transaction Date"
        },
        status: {
            register: "Registered",

            rejected: "Deregistered",
            expired: "Expired",
        },
        filter: {
            status: {
                all: "All Status",

                registered: "Registered",
                rejected: "Deregistered",
                expired: "Expired",

                pending: "Pending",
                certificated: "Certified",
            },
            type: "All Type",
            province: "All Province",
            co2Min: "Min ",
            co2Max: "Max ",
            search: "Search",
            type_to_search: "Type to search",
            limit: "Show {limit}",
            saperate: "to",
            all_standard: "All Standard",
            all_external_assessors: "All Validation/Verification Body",
            all: 'All',
            label: {
                status: "Project Status",
                sub_status: "Credit Status",
                standard: "Standard",
                type: "Project Type",
                carbon_credit_amount: "Carbon Credit Amount",
                crediting_peroid: "Crediting Peroid",
                external_assessors: "Validation/Verification Body",
                corsia: 'Authorized Use',
                block_range: "Credit Number",
                cancellation_reason_types: "Cancellation Purpose",
                "Cooperative Approach": "Cooperative Approach",
                transaction_date: "Transaction Date",
                vintage_year: "Vintage Year",
            },
        },
    },
    view_page: {
        page_title: "Project Details",
        project_id: "Project ID",
        project_overview: "Project Overview",
        project_overview_lang: {
            th: "Project Overview (Thai)",
            en: "Project Overview (ENG)",
        },
        project_type: "Project Type",
        knp_rule: "CCMGM Project Type",
        project_owner: "Project Owner",
        project_developer: "Project Developer",
        project_owner_lang: {
            th: "Project Owner (Thai)",
            en: "Project Owner (ENG)",
        },
        project_developer_lang: {
            th: "Project Developer (Thai)",
            en: "Project Developer (ENG)",
        },
        external_assessors: "Validation/Verification Body",
        external_assessors_lang: {
            th: "Validation/Verification Body (Thai)",
            en: "Validation/Verification Body (ENG)",
        },
        registered_date: "Registration Date",
        credit_period_project: "Crediting Period",
        standard: "Standard",
        project_images: "Project Images",

        registered_doc: "Registration Documents",
        additional_doc: "Other Documents",
        filename: "Filename",
        file_type: "File Type",
        project_status: "Project Status",
        cancelled: "Cancelled",
        expired: "Expired",
        registered: "Registered",
        adress_position_title: "Location List ({amount} locations)",
        estimated_greenhouse_gases_reduction: "Estimated Greenhouse Gas Reduction/Removal (tCO<sub>2</sub>eq/year)",
        approved_carbon_credits: "Issued Carbon Credits (tCO<sub>2</sub>eq)",
        carbon_credits_verified_table: "Carbon Credits Certification",
        credit_period: "Crediting Period",
        greenhouse_gases_amount_approve: "Documents",
        status_certificate_carbon: 'Status',

        certicate_carbon: {
            certified_carbon_credit: 'Certified Carbon Credits',
            document: 'Documents',
            status: 'Status',
            quantity: 'Amount',
            percent_buffer:'Buffer',
            issuance_date:'Issuance Date',
            cancellation:'Cancellation Credit'

        },
        total: "Total",
        co_benefit: "Co-Benefits",
        co_benefit_lang: {
            th: "Co-Benefits (Thai)",
            en: "Co-Benefits (ENG)",
        },
        environmental: "Environmental",
        societal: "Social",
        economical: "Economic",
        latitude: "Latitude",
        longitude: "Longitude",
        ton: "Ton",
        pending_approval: "Pending approval",
        sum: "Sum",
        Click_to_select_a_file: "Click to select a file",
        or_drag: "or drag the file down here",
        amount: "Amount",
        message_to_user: "Message to user",
        start_date: "Start date",
        end_date: "End date",
        programid: 'Program ID',
        authorizeduse: 'Authorized Use',
        vintage_start: "Start year",
        vintage_end: "End year",
        account:'Account',
        reference_link:'Reference Link'
    },
    create_page: {
        programid: 'Program ID',
        authorizeduse: 'Authorized Use',
        page_title: "Create Project",
        project_id: "Project ID",
        project_name: {
            th: "Project Name (Thai)",
            en: "Project Name (ENG)",
        },
        dropdowns: {
            project_type: "select project type",
            project_type_ccmgm: "select CCMGM project type",
        },
        address: {
            title: "Project Address",
            subtitle: "Address",
            subtitle_lang: {
                th: "Address (Thai)",
                en: "Address (ENG)",
            },
        },
        project_type: "Type",
        knp_rule: "Type according to CCMGM",
        project_owner: "Project Owner",
        project_developer: "Project Developer",
        project_owner_lang: {
            th: "Project Owner (Thai)",
            en: "Project Owner (ENG)",
        },
        project_developer_lang: {
            th: "Project Developer (Thai)",
            en: "Project Developer (ENG)",
        },

        external_assessors: "Validation/Verification Body",
        external_assessors_lang: {
            th: "Validation/Verification Body (Thai)",
            en: "Validation/Verification Body (ENG)",
        },
        registered_date: "Registration Date",
        standard: "Standard",
        project_images: "Project Images",

        credit_period_project: "Crediting Period",
        project_investment: "Total Investment (mTHB)",
        reduction_methods: {
            title: "Applied Methodologies",
            name: "Document Name",
            document_version: "Document Version",
            description: "Descriptions",
        },

        registered_doc: "Registration Documents",
        additional_doc: "Other Documents",

        filename: "Filename",
        file_type: "File Type",
        project_status: "Project Status",
        estimated_greenhouse_gases_reduction: "Estimated Greenhouse Gas Reduction (tCO<sub>2</sub>eq/year)",
        approved_carbon_credits: "Issued Carbon Credits (tCO<sub>2</sub>eq)",
        carbon_credits_verified_table: "Carbon Credits Certification",
        credit_period: "Crediting Period",
        greenhouse_gases_amount_approve: "Documents",
        total: "Total",
        co_benefit: "Co-benefit",
        environmental: "Environmental",
        societal: "Social",
        economical: "Economic",
        latitude: "Latitude",
        longitude: "Longitude",
        ton: "Ton",
        pending_approval: "Pending approval",
        sum: "Sum",
        Click_to_select_a_file: "Click to select a file",
        or_drag: "or drag the file down here",
        amount: "Amount",
        message_to_user: "Message to user",
        start_date: "Start date",
        end_date: "End date",
        vintage_year: 'Year',

        form_validation: {
            project_name: "Please fill project name.",

            address: "Please fill project address",
            project_type: "Please select project type",
            knp_rule: "Please fill type according to CCMGM",
            project_owner: "Please fill project owner name",
            external_assessors: "Please fill Validation/Verification Body",
            project_developer: "Please fill project developer name",
            registered_date: "Please fill registration Date",
            credit_period_project: "Please fill crediting period",
            project_investment: "Please fill project investment",
            standard: "Please select project standard",

            reduction_methods: {
                name: "Please fill document name",
            },

            estimated_greenhouse_gases_reduction: "Please fill Estimated Greenhouse Gas Reduction/Removal (tCO<sub>2</sub>eq/year)",

            co_benefit: "Please fill co benefit",
            environmental: "Please fill co benefit environmental",
            societal: "Please fill co benefit Social",
            economical: "Please fill co benefit Economic",
            latitude: "Please fill co benefit latitude",
            longitude: "Please fill co benefit longitude",
            project_type_by_extens: "",
            project_activity: "Please fill project detail",

            certificated_carbon_credit: {
                certification_date: "Please fill certification date.",
                start_date: "Please fill start date.",
                end_date: "Please fill end date.",
                credit: "Please fill credit amount.",
                file: "Please upload file.",
            },
            programid: "Please fill program id",
            authorizeduse: "Please fill authorized use",
        },
    },
};