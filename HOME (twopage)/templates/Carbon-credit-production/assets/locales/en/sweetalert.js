export default {
	confirm_correction: "Confirm correction",
	Please_confirm_the_correction: "Please confirm the correction",
	confirm: "Confirm",
	cancel: "Cancel",
	Correction_succeeded: "Correction succeeded",

	confirm_creation: "Confirm Creation",
	Please_confirm_the_creation: "Please confirm the creation.",
	creation_success: "Create project successful!",
	complete_information_text: "Please check your infoemation and try again",
	complete_information: "Please completed your information",

	invalid: "Invalid",
	error: "Error",
	successful: "Successful",
	fail: "Fail",
	confirm_certificate: {
		title: "Confirm Certification",
		text: "Complete information and confirm credit certification.",
	},
	waiting: "Please Wait",
	

	transferModal: {
		title: {
			success: "Transaction in Progress.",
			error: "Transaction Fail",
			invalid: "Invalid Information",
			confirm: "Confirm Transaction",
		},
		text: {
			success: "Pending for administrative approval.",
			error: "Insufficient carbon credit.",
			invalid: "Please fill out the required information.",
			confirm: "Please confirm the transaction.",
		},
	},

	transaction: {
		approval: {
			title: {
				confirm_approve: "Confirm Approve",
				success_approve: "Approve Success",
				error_approve: "Approve Fail",

				confirm_reject: "Confirm Rejection",
				success_reject: "Rejection Success",
				error_reject: "Rejection Fail",
			},
			text: {
				confirm_approve: "This action cannot be undone. This will approve the transaction request.",
				success_approve: "",
				error_approve: "Approve transaction fail. Please try again",

				confirm_reject: "This action cannot be undone. This will reject the transaction request.",
				success_reject: "",
				error_reject: "Rejection transaction fail. Please try again",
			},
			input: {
				label1: "Message Detail (optional)",
				label2: "Message Detail (require)",
				placeholder: "message...",
				error_msg: "Please fill reject reason.",
			},
		},
		setting: {
			confirm: {
				title: "Confirm Setting",
				sub_title: "This action will be apply after your confirm to {action} auto approve entire transactions.",
			},
			success: {
				enabled: {
					title: "Enable success",
					sub_title: "The auto approve has been Enabled",
				},
				disabled: {
					title: "Disable success",
					sub_title: "The auto approve has been diabled",
				},
			},
			error: {
				title: "Setting Fail",
				sub_title: "Please try agian.",
			},
		},
	},
	account: {
		input: {
			label1: "Message Detail (optional)",
			label2: "Message Detail (require)",
			placeholder: "message...",
			error_msg: "Please fill reject reason.",
		},
		
	},
	api: {
		create: {
			title: "Confirm Creation",
			sub_title: "Please confirm your API creation",
		},
		edit: {
			title: "Confirm Creation",
			sub_title: "Please confirm your API creation",
		},
		delete: {
			title: "Confirm Creation",
			sub_title: "Please confirm your API creation",
		},
		reset: {
			title: "Confirm reset secret key",
			sub_title: "Please confirm reseting secret key",
			success: "Reset secret key success.",

			error: "Reset secret key fail.",
		},
		success: {
			title: "Create Successful",
			sub_title: "Please copy the Access key and Secret key for authorization",
		},
		error: {
			title: "Create Fail",
			sub_title: "Creation has been fail, Please try again.",
		},
	},
	profile: {
		change_password: {
			confirm: {
				title: "Confirm",
				sub_title: "Please confirm your change",
			},
			success: {
				title: "Change Password Success",
				sub_title: "",
			},
			error: {
				title: "Change Password Fail",
				sub_title: "",
			},
		},
	},

	user: {
		edit: {
			confirm: {
				title: "Confirm Edit",
				sub_title: "Are you sure you want to edit the information of this user?",
			},
			success: {
				title: "Edit Success",
				sub_title: "User information has been change.",
			},
			error: {
				title: "Edit Failed",
				sub_title: "Failed to edit data. Please try again.",
			},
		},
		create: {
			confirm: {
				title: "Confirm Create",
				sub_title: "Please confirm the creation of the new user account.",
			},
			success: {
				title: "Create Success",
				sub_title: "Create new user success",
			},
			error: {
				title: "Create Failed",
				sub_title: "Create new user failed. Please try again.",
			},
		},
	},
	auth:{
		forgotPassword:{
			success: {
				title: "Completed!",
				sub_title: "We’ve sent a link reset password to your email.",
			},
			error: {
				title: "Failed",
				sub_title: "Failed to request change password. Please try again.",
			},
		},
		newPassword:{
			success: {
				title: "Completed!",
				sub_title: "Your password has been changed. Please login with the new password.",
			},
			error: {
				title: "Failed!",
				sub_title: "Failed to change password. Please try again.",
			},
		}
	},
	project:{
		certifiedCredit:{
			confirm: {
				title: "Confirm certification",
				sub_title: "Please confirm carbon credit certification",
			},
			success: {
				title: "Certification successful",
				sub_title: "The system has certified {amount} carbon credits for you.",
			},
			error: {
				title: "Certification unsuccessful",
				sub_title: "Carbon credit certification failed. Please try again.",
			},
		}
	},

	openAccount:{
		confirm: {
			title: "Confirm account opening",
			sub_title: "Please confirm the information for opening a carbon credit account.",
		},
		success: {
			title: "Operation completed successfully.",
			sub_title: "Pending approval from the officer. Once the officer completes the process, the system will notify you via email.",
		},
		error: {
			title: "The operation was unsuccessful.",
			sub_title: "The account opening process was unsuccessful. Please try again.",
		},
	},
	checkout:{
		confirm: {
			title: "Comfirm Purchase",
			sub_title: "Please confirm your purchasing.",
		},
		success: {
			title: "Purchase successful",
			sub_title: "อยู่ระหว่างรออนุมัติจากเจ้าหน้าที่ เมื่อเจ้าหน้าที่ดำเนินการแล้ว ระบบจะแจ้งเตือนไปยังอีเมลของท่าน",
		},
		error: {
			title: "Purchase fail",
			sub_title: "Please try again",
		},
	},
	buffer:{
		confirm: {
			title: "Comfirm Issue",
			title2: "Comfirm",
			sub_title: "Please confirm your carbon Issue.",
			sub_title2: "Please confirm your reversal retirement process.",
		},
		success: {
			title: "Issued successful",
			title2: "successful",
			sub_title: "อยู่ระหว่างรออนุมัติจากเจ้าหน้าที่ เมื่อเจ้าหน้าที่ดำเนินการแล้ว ระบบจะแจ้งเตือนไปยังอีเมลของท่าน",
		},
		error: {
			title: "Issued fail",
			title2: "Fail",
			sub_title: "Please try again",
		},
		input:{
			label:'Remark',
			placeholder:'Message',
		}
	}
};
