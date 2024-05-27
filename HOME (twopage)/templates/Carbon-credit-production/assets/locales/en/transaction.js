export default {
	page_title: "Transaction",
	
	setting:{
		auto_approve:'Automatic Approval'
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
			project_id: "Project ID",
			project_title: "Account Name",
			sender:'Carbon Credit Provider',
			receiver:'Carbon Credit Receiver',
			amount:'Transfer Amount',
			status:'Status',
			date:'Transfer Date',
			no:'No.'
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
