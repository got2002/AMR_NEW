export default {
	page_title: "API Credentials",
	unit:{
		item:'items'
	},
	stat_title: {
		all: "Total Aliases",
		enable: "Available",
		disable: "Suspended",
	},
	filter: {
		status: {
			all: "Status",
			draft: "Draft",
			released: "Released",
			terminated: "Terminated",
			temporary_close: "Temporary Closed",
		},
		search: "Search",
		limit: "Show {limit}",
	},
	table: {
		header: {
			alias_name: "Alias name",
			email: "Email",
			permission: "Permissions",
			status: "Status",
			created_date: "Created At",
			last_used: "Last Used",
			tools: "Tools",
		},
	},
	create_page: {
		page_title: "Create new credential",
		manual: {
			_0: "User Manual for Credential usages",
			_1: `When you have successfully created a 'Credential API', you will receive an 'Access Key' and a 'Secret Key`,
			_2: `Your endpoint system is required to submit both the 'Access Key' and 'Secret Key' to authenticate and receive a 'JWT Token' which will be valid for 1 hour.`,
			_3: `The 'JWT Token' can be used to access the API as prescribed.`,
		},
		form:{
			alias_name:'Alias Name',
			full_name:'Full Name',
			email:'Email',
			purpose_description:'Purpose/Description',
			account_number:'Account Number',
			api_permission:'API Permissions',

		},
		permissionCheck:{
			all_project_pagination:'All projects pagination',
			all_project_pagination_for_transfer:'All projects pagination for transfer',
			get_project_by_id:'Get project by ID',
			create_project:'Create a project',
			update_project:'Update a project',
			transfer_credit:'Transfer credits',
			retirement_credit:'Retirement credits',
			all_account_number:'All account number',
			all_credit_wallet:'All credit wallet',
			all_credit_transaction:'All credit transaction',
			user_sync_token:'User sync token'
		}
	},
	edit_page: {
		page_title: "Credential Information",
		manual: {
			_0: "User Manual for Credential usages",
			_1: `When you have successfully created a 'Credential API', you will receive an 'Access Key' and a 'Secret Key`,
			_2: `Your endpoint system is required to submit both the 'Access Key' and 'Secret Key' to authenticate and receive a 'JWT Token' which will be valid for 1 hour.`,
			_3: `The 'JWT Token' can be used to access the API as prescribed.`,
		},
	},
};
