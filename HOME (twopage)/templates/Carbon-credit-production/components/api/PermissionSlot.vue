<template>
	<td class="border-t-0 px-3 text-sm border-l-0 border-r-0 whitespace-nowrap bg-white" >
		<div class="flex w-full h-full gap-4" :class="{ 'justify-start': align == 'left', 'justify-center': align == 'center' }">
			

			<input type="checkbox" name="permission" :value="itemValue" v-model="form.scopes" class="w-4 h-4 bg-gray-100 rounded-sm">
		</div>

		<!-- <i class="fa-solid fa-pen-to-square"></i> -->
	</td>
</template>

<script>
export default {
	props:['itemValue','align','form'],

	mounted() {},
	methods: {
		deleteItem() {
			const app = this
			this.$swal
				.fire({
					
					icon:'warning',
					title: this.$t("alertBox.title.doYouWantToDelete"),
					showDenyButton: false,
					showCancelButton: true,
					confirmButtonText: this.$t("button.confirm"),
					confirmButtonColor: "#185ea6",
					cancelButtonText: this.$t("button.cancel"),
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$axios
							.$delete(`https://api.hotel.optemis.space/api/v1/license/${app.id}` )
							.then(function () {
								app.$toast.success(app.$t("word.saved"));
								setTimeout(app.$toast.clear, 3000);
								app.$router.push(app.localePath({ name: "admin-datatables-permitList" }));
								app.$emit('fetchData')
							})
							.catch(function () {
								app.$toast.error(`${app.$t("word.error")}`);
								setTimeout(app.$toast.clear, 3000);
							});
					}
				});
		},
	},
};
</script>
