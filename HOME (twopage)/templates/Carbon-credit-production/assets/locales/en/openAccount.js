export default {
    openAccount: "Open a new account (เปิดบัญชีใหม่)",
    serviceAgreement: "Carbon Credit Account Opening Service Agreement",
    accept: "Accept",
    refuse: "Refuse",
    accountName: "Account Name",
    email: "Email",
    firstname: "Firstname",
    lastname: "Lastname",
    organization: "Organization",
    password: "Password",
    passwordConfirmation: "Password Confirmation",
    document: "Upload documents",
    chooseAfile: "Choose a file or drag a file here",
    onlyPDF: "(Only PDF files are supported)",
    instructions: "Instructions for opening a new account",
    confirm: "Confirm the information is correct",
    accountOpening: "Account opening takes approximately 1-3 business days to process if your account has been approved. The system will send an account opening notification to the specified email address",
    cancel: "Cancel",
    submit: "Submit",
    accountType: 'Account Type',
    showDocument: {
        title: 'Document',
        card_id: 'Copy of Thai National ID Card or Passport',
        verified: 'Certificate of juristic person issued by the Department of Business Development, Ministry of Commerce, certified by the registrar not more than 3 months.',
        verified1: 'Copy of the law or related documents showing the establishment of an organization',
        authorize: 'Power of attorney letter for the authorized person (system user).',
        card_id_owner: 'Copy of the national identification card or passport of the person granting the power of attorney.',
        card_id_representative: 'Copy of the national identification card or passport of the authorized person.',
        employment_certificate: 'Employment verification letter issued by the company.'
    },
    stepbar: {
        step1: 'Accont type',
        step2: 'Agreement',
        step3: 'Application form',
        step4: 'Upload file',
        step5: 'Review',
    },
    validate: {
        document: 'Please attach document file',
        accountName: "Please specify an account name",
        containsNotSpecial: "Do not use special characters",
        minLength2: "Please specify 2 or more characters",
        email: "Please specify email",
        emailValidate: "invalid email",
        firstname: "Please specify firstname",
        lastname: "Please specify lastname",
        organization: "Please specify organization",
        password: "enter password",
        minLength8: "Please specify 8 or more characters",
        passwordConfirmation: "Passwords do not match",

        id_card: "Please provide your national identification card/passport number.",
        phone_number: "Please provide the phone number.",
        address: "Please provide your current address.",
        province: "Please specify the province.",
        district: "Please specify the district.",
        subdistrict: "Please specify the sub-district/ward.",
        postcode: "Please specify the postal code.",
        requestPermission: "Please specify the type of account applicant (at least 1 type).",

        juristic: {
            name: 'Please specify an juristic name',
            office_address: 'Please provide your office address.'
        },
        government: {
            name: 'Please specify an organization name',
            office_address: 'Please provide your organization address.'
        },
        account_type: 'Please specify the account type.',
        role: 'Please specify the role.',
    },
    form: {
        title: "The application form for requesting to open an account in the carbon credit registry system.",
        guest: {
            subtitle: "The type of general user.",
        },
        juristic: {
            subtitle: "The type of juristic.",
            name: "Name of the juristic person, group of persons, or association.",
            address: "Office address.",
            number: "Company registration number (if available).",
            alien_id: "Work permit number of foreigner",
            alien_id_description: "(In case of foreigner who needs to apply for a work permit for foreigner to operate business)",
            grantee_info: {
                title: "Representative or authorized person for conducting transactions in the carbon credit registry system.",
            },
            account_detail: {
                title: "Account details.",
            },
        },
        government: {
            subtitle: "The type of government.",
            name: 'Organization name',
            address: 'Office Address',


            grantee_info: {
                title: 'Representative or authorized person for conducting transactions in the carbon credit registry system.',

            },
            account_detail: {
                title: 'Account details',

            }
        },

        firstname: "Firstname",
        lastname: "Lastname",
        card_id: "national identification card/passport number.",
        issued_by: "Issued by (in case of foreign passport)",
        phone_number: "Phone Number",
        email: "Email",
        password: "Password",
        passwordConfirmation: "Confirm Password",
        address: "Address",
        province: "Province",
        district: "District",
        subdistrict: "Subdistrict",
        postcode: "Postcode",
        accountName: "Account name (in English letters based on the name and surname of the applicant).",
        request_permission: {
            title: "Type of account applicant (can choose more than 1 type)",
            item1: "Project developer or owner of greenhouse gas reduction project.",
            item2: "Person who intends to purchase or transfer carbon credits.",
            item3: "The person who has received carbon credits through a carbon credit exchange center.",
        },
        document: {
            card_id: "Upload a copy of the national identification card.",
            verified: "Certificate of juristic person issued by the Department of Business Development, Ministry of Commerce, certified by the registrar not more than 3 months.",
            verified1: 'Copy of the law or related documents showing the establishment of an organization',
            authorize: "Power of attorney letter for the authorized person (system user).",
            card_id_owner: "Copy of the national identification card or passport of the person granting the power of attorney.",
            card_id_representative: "Copy of the national identification card or passport of the authorized person.",
            employment_certificate: "Employment verification letter issued by the company.",
        },
    },

    agreement: {
        title: "Agreement for the service of applying for a carbon credit account.",
        sentense: "Consent form for the collection, use, or disclosure of personal information by the management organization of greenhouse gas (corporation).",
        sentense1: `TGO will collect, use, and disclose my personal information that I have provided directly when submitting a request to open an account in the Carbon Credit Registration System or that arises during any stage of TGO's consideration process. This includes my name, national ID card number or passport number, photograph, address, email, signature, nationality, gender, and any other information that appears in the documents submitted to TGO or documents that TGO has obtained. I hereby consent to the collection, use, and disclosure of my personal information by TGO as follows:`,
        p1: `1. Please let TGO and its staff use my personal data collected for the purpose of communication and public relations related to activities promoting capacity building or any other activities related to TGO's mission.`,
        p2: `2. Allow the TGO to disclose my personal information, including name, position, and public contact information, such as the TGO website or other channels of the organization.`,
        p3: `3. Allow the TGO to disclose my personal information to data processors appointed by the OGA for the purpose of conducting studies, research, development, improvement of systems, or any other operations related to the TGO's mission within the scope of the personal data processing agreement.`,
        p4_1: "I understand that I am entitled to withdraw any and all of my consent given in this form at any time by submitting the withdrawal form provided by TGO and shall clarify the reasons of such withdrawal to TGO.",
        p4_2: "My withdrawal shall not affect any action taken by TGO prior to receiving and processing my withdrawal.",
        p4_3: "In case of withdrawal, I understand and accept any consequence which may affect my rights or obligations relating to the service provided by TGO.",
        p4_4: "I have read and acknowledged TGO’s privacy notice and hereby signed this consent form."
    },

    account_type: {
        title: "Select Account Type",
        subtitle: "Please select the type of account you want to open",
        option: {
            guest: "General",
            juristic: "Juristic",
            government: "Government or State-owned enterprise",
        },
        document_discription: {
            title: "Account Opening Supporting Documents",
            guest: {
                title: "In the case of the general public",
                // item1: "Application form for opening a carbon credit trading account by specifying the email to be used in the system",
                item1: "Copy of ID card",
            },
            juristic: {
                title: "In the case of juristic persons, groups of individuals, or associations of individuals.",
                // item1: "Application form for opening a carbon credit trading account by specifying the email to be used in the system.",
                item1: "Name, address, and a certification letter issued by the Department of Business Development, Ministry of Commerce, certified not more than 3 months ago.",
                item2: "Power of attorney letter given to the authorized person (system user).",
                // item4: "Copy of ID card or passport of the grantor.",
                item3: "Copy of ID card or passport of the grantee.",
                // item6: "Employment certificate issued by the company.",
            },
            government: {
                title: "In the case of state agencies, government entities, or state enterprises.",
                // item1: "Application form for opening a Carbon Credit Trading Account, specifying the email address to be used in the system.",
                item1: "Name, address, and a copy of the law or relevant evidence indicating the establishment of the organization.",
                item2: "Letter of authorization for the authorized person (system user).",
                // item4: "Copy of the ID card or passport of the authorizing person.",
                item3: "Copy of the ID card or passport of the authorized person.",
            },
        },
    },
};