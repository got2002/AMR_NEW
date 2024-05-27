export default {
    role: {
        admin: "Admin",
        registrar: "Registrar",
        user: "User",
    },
    page_title: "List of User Accounts",
    statCO2VolumeTitle: {
        all: "Accounts",
        organization: "Organizations/Affiliations",
        approved: "Approved",
        pending: "Waiting for Approval",
        rejected: "Rejected",
    },
    filter: {
        role: {
            all: "All Role",
            user: "Status",
            admin: "Admin",
            moderator: "Moderator",
        },
        status: {
            pending: "Pending",
            approved: "Approved",
            all: "All Status",
        },
        organization: "Organization/Affiliation",
        search: "Search",
        limit: "Show {limit}",
    },
    table: {
        header: {
            user_id: "Account order",
            name: "Name",
            email: "Email",
            organization: "Organization/Affiliation",
            role: "Role",
            status: "Status",
            registere_date: "Registered",
            last_login: "Last Login",
            tool: "Tools",
        },
    },
    view: {
        page_title: "User Account Information",
        approve_page_title: "Request Information",
        form: {
            profile_title: 'general information',
            account_title: 'credit account information',
            document: 'documents',
            part: 'part {number}'
        }
    },
    create_page: {
        page_title: "Create user account",
        subtitle: "Please completed your information",
        form: {
            title: "Personal Information",
            firstname: "Firstname",
            lastname: "Lastname",
            organization: "Organization/Affiliation",
            role: "Role",
            email: "Email",
            password: "Password",
            confirm_password: "Confirm Password",
            permission: "Permission",
            dropdowns: {
                organization: {
                    all: "Select Organization",
                },
                role: {
                    all: "Select Role",
                },
            },
            account_type: "Account Type",
        },
    },
    change_password_tab: "Password",
    change_password_sent_mail_option: "Generate and send to email",
    change_password_sent_mail_option_button: "Send",
    change_password_typing_option: "Set the new password",
    change_password_sent_mail_message: "The system will randomly generate a password and send the new password to the email <span class='font-bold'>{email}</span> after the process is completed. The system will then change the password immediately. Please verify the accuracy of the email before proceeding each time.",
};