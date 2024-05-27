export default {
    methods: {
        async uploadImages(formData) {
          
            return await this.$axios
                .$post(`/api/v1/form/upload`, formData)
                .then((resp) => {
                    // console.log(resp);
                    return resp
                })
                .catch((err) => {
                    console.log(err);
                });
            // const reader = new FileReader();
            // reader.onload = function (e) {
            //     app.fileArr.push(e.target.result);
            // };

            // reader.readAsDataURL(fileItem);

        },
    }
}