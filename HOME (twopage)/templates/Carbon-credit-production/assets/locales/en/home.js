export default {
	modal: {
		title: "Account Code",
		subtitle: 'The confirmation code is used to link accounts between the Thailand Greenhouse Gas Management Organization (TGO) and the Carbon Credit Trading System (FTIX). The code will be valid for 1 Day. If the code has expired, you can create a new password by clicking the "Create New Code" button.',

		label: {
			token: "Code",
		},
		request_statement_title: "Request Statement",
		filter: {
			month: "Select Month",
			language: "Language",
			placeholder: "From - To",
			placeholder2: "click for select",
			email: "Email",
		},
	},
	account:{
		pending_status:'Pending Account'
	},
	title: {
		credit_list: "credit list",
		transaction_history: "transaction history",
		account_number: "Account Number",


		account_list:'Account',
		new_account:'New Account'
	},
	table: {
		title: "Example Data",
		header: {
			datetime: "Date/time",
			transferor: "Transferor",
			transferee: "Transferee",
			credit_amount: "Credit Amount",
			remark: "Remark",
		},
	},
	form_validation: {
		date: "Please fill month",
		lang: "Please fill document language",
		email: "Please fill email address",
	},
	swal: {
		statement: {
			title: {
				success: "Success",
				invalid: "Invalid",
				error: "Error",
			},
			text: {
				success: "The statement has been send to your email",
                check_email:'Please check your email box at {email}',
				invalid: "Please complete the data before submittion.",
				error: "Requestion has been fail. Please try again",
			},
		},
	},
};
