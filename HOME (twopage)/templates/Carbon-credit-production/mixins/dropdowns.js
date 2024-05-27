export default {
    methods: {
        async getProjectTypesBBR() {
            return await this.$axios
                .$get(`/api/v1/dropdown/project-types-abbr`)
                .then((resp) => resp)
                .catch((errors) => {
                    console.log(errors);
                });
        },
        async getDropdownProgramID() {
            return await this.$axios
                .$get(`/api/v1/dropdown/programids`)
                .then((resp) => resp)
                .catch((errors) => {
                    console.log(errors);
                });
        },
        async getDropdownAutherizedUse() {
            return await this.$axios
                .$get(`/api/v1/dropdown/authorizeduses`)
                .then((resp) => resp)
                .catch((errors) => {
                    console.log(errors);
                });
        },

        async getDropdownStandard() {
            return await this.$axios
                .$get(`/api/v1/dropdown/projectstandardids`)
                .then((resp) => resp)
                .catch((errors) => {
                    console.log(errors);
                });
        },
        async getProjectTypes() {
            return await this.$axios
                .$get(`/api/v1/dropdown/project-type-by-extends`)
                .then((resp) => resp)
                .catch((errors) => {
                    console.log(errors);
                });
        },
        async getAccount() {
            return await this.$axios
                .$get(`/api/v1/dropdown/account-numbers`)
                .then((resp) => resp)
                .catch((errors) => {
                    console.log(errors);
                });
        },
        async getCancellationReason() {
            return await this.$axios
                .$get(`/api/v1/dropdown/cancellation-reason-types`)
                .then((resp) => resp)
                .catch((err) => console.log(err));
        },
        async getITMOsCancellationReason() {
            return await this.$axios
                .$get(`/api/v1/dropdown/itmos-cancellation-reason-types`)
                .then((resp) => resp)
                .catch((err) => console.log(err));
        },
        async getAccountDropdowns(type = "") {
            // console.log("sds");

            return await this.$axios
                .$get(`/api/v1/dropdown/account-numbers?transaction_type=${type}`)
                .then((resp) => resp)
                .catch((err) => console.log(err));
        },
    },
};