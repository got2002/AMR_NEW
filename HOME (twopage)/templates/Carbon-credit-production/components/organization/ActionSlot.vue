<template>
	<th class="py-2 text-center flex items-center justify-center gap-2">
		<nuxt-link :to="localePath({ name: 'organization-id-edit', params: { id: id } })">
			<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-yellow-500">
				<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
			</svg>
		</nuxt-link>
		<button @click="deleteUser(id)">
			<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash text-red-500" viewBox="0 0 16 16">
				<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
				<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
			</svg>
		</button>
	</th>
</template>

<script>
	export default {
		props: {
			id: {
				type: String,
				default: () => "",
			},
		},
		methods: {
			deleteUser(id) {
				const app = this;
				this.$swal
					.fire({
						icon: "info",
						iconColor: "#ef4444",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
								</svg>`,
						title: this.$t("alert.title.warning"),
						text: this.$t("alert.text.warning.delete"),
						showCancelButton: true,

						confirmButtonColor: "#ef4444",
						confirmButtonText: this.$t("button.confirm"),
						cancelButtonText: this.$t("button.cancel"),
						reverseButtons: true,
					})
					.then((result) => {
						if (result.isConfirmed) {
							app.$swal.fire({
								title: this.$t("sweetalert.waiting"),
								text: this.$t("deleting"),
								allowOutsideClick: false,
								showCloseButton: false,
							});
							app.$swal.showLoading();
							app.$axios
								.$delete(`/api/v1/organization/${id}`)
								.then((resp) => {
									// console.log(resp);

									// app.form = resp;
									app.$swal.close();
									app.$swal
										.fire({
											icon: "success",
											iconColor:'#059669',
											confirmButtonColor: "#059669",
											title: this.$t("alert.title.success.delete"),
											timer: 2000,
											timerProgressBar: true,
										})
										.then(() => {
											app.$emit("reload");
										});
								})
								.catch((err) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "error",
										title: this.$t("alert.title.error.delete"),
									});
									console.log(err);
								});
						}
					});
			},
		},
	};
</script>

<style></style>
