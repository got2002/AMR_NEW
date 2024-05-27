export default {
    require: {
        firstname: "Please fill firstname.",
        lastname: "Please fill lastname.",
        organization: "Please select organization",
        role: "Please select role",
        email: "Please fill email.",
        password: "Please fill password",
        confirm_password: "Please fill confirm password",
        accountTypes: "Please select account types",
        transactionTypes: "Please select transaction types",
        Accountname: "Please fill account name",
        account_type: "Please select account type",
    },
    min_length: {
        firstname: "The firstname length  must be at least 2 character",
        lastname: "The lastname length  must be at least 2 character",
        password: "The password must be at least 8 character",
        Accountname: "The account name length  must be at least 2 character",
    },
    same_as: {
        confirm_password: `Confirm password doesn't match.`,
    },
    pattern: {
        email: "Please enter a valid email address",
        firstname_contain_special: "The firstname must not contain special character",
        lastname_contain_special: "The lastname must not contain special character",
        Accountname: "The account name must not contain special character",
    },
    strong_password: "Password must contain uppercase and lowercase letters. numbers and symbols It consists of a number greater than or equal to 8 characters.",

    min_max: 'The carbon amount must be greater than {min} and less than or equal to {max}.'
};