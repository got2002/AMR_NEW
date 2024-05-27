export default {
	page_title: "List of Credit Accounts",
	button:{
		remove:'Remove'
	},
	statCO2VolumeTitle: {
		all: "Accounts",
		organization: "Organizations/Affiliations",
		approved: "Approved",
		pending: "Waiting for Approval",
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
		addAccount: "Add Account",
	},
	table: {
		header: {
			account_id: "Account Number",
			name: "Account Name",
			credit: "Total Credit",
			tool: "Tools",
			accountType: "Account Type",
			createAt: "Registered",
			number_of_projects: "Number of projects",
		},
	},
	accountType:{
		guest:'Guest',
		juristic:'juristic',
		government:'Government'
	},
	card:{
		attach_files:'Attach Files ({item})',
	},
	view: {
		page_title: "Credit Account Information",
		table_credit_balance: "Credit Balanc",
		year: "Year",
		quantity: "Quantity",
		date_and_time: "Date and Time",
		detailed: "Detailed",
		transferor: "Transferor",
		transferee: "Transferee",
		credit: "Credit",
		transaction: "Carbon transaction history",
		transfer: "Transfer",
		status: "status",

	},
	create_page: {
		page_title: "Create credit account",
		subtitle: "Please completed your information",
		form: {
			title: "Account Information",
			firstname: "Firstname",
			lastname: "Lastname",
			organization: "Organization/Affiliation",
			role: "Role",
			email: "Email",
			password: "Password",
			confirm_password: "Confirm Password",
			permission: "Permission",
			dropdowns: {
				accountTypes: {
					all: "Select Account Types",
				},
				transactionTypes: {
					all: "Select Transaction Types",
				},
				email: {
					all: "Select Email",
				},
			},
			name: "Account Name",
			accountTypes: "Account Types",
			transactionTypes: "Transaction Types",
		},
	},
	transfer: {
		project_number: "Project number",
		project_name: "Project name",
		please_select_a_project: "Please select a project",
		remark: "Remark",
		transfer: "Transfer",
		Please_select_a_transferee: "Please select a transferee",
		Do_you_want_to_transfer_credit: "Do you want to transfer credit",
		successful_transfer: "Successful transfer",
		carbon_credit_transfer: "Carbon credit transfer",
	},
};
