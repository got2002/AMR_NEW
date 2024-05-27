<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 2xl:overflow-hidden overflow-x-scroll shadow-sm rounded">
		<table class="items-center w-full space-y-6 shadow-sm rounded-sm">
			<thead>
				<tr>
					<template v-for="(header, idx) in tHead">
						<AccountHeaderSlot :header="header" :key="idx" @setSort="setSort(header.sortKey,$event,idx)"/>
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in tData">
					<tr tabindex="0" :class="{ 'bg-gray-100': index % 2 == 1 }" class="focus:outline-none text-xs h-12 rounded" :key="index">
						<AccountTDSlot :text="data.desAccountNumber" align="" />
						<AccountTDSlot :text="data.desAccountNumber" align="">
							<AccountNameEdit :data="data" @edit="editName(data._id,$event)"/>
						</AccountTDSlot>
						<AccountTDSlot :text="groupedProject(data.accountVintages)" align="center" />
						<AccountTDSlot :text="data.totalCredits?.toLocaleString()" align="center" />
						<AccountTDSlot :text="dateLocale(data.createdAt)" align="center" />
						<AccountTDSlot text="" align="center">
							<div class="w-full flex items-center justify-center gap-2">
								<nuxt-link :to="localePath({ name: 'accounts-id', params: { id: data._id } })">
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-blue-500">
										<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
										<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
									</svg>
								</nuxt-link>

								<button @click="deleteUser(data._id)">
									<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash text-red-500" viewBox="0 0 16 16">
										<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
										<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
									</svg>
								</button>
							</div>
						</AccountTDSlot>
						
					</tr>
				</template>
			</tbody>
		</table>
	</div>
</template>

<script>

export default {
	props: {
		tHead: {
			type: Array,
			require: true,
		},
		tData: {
			type: Array,
			require: true,
		},
	},
	data() {
		return {
			edit: [],
		};
	},
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	mounted() {
		
	},
	methods: {
		async setSort(key,value,index){
			await this.tHead.map((item,idx)=>{
				if(idx !== index){
					item.sortValue = 0
					
				}
				// console.log(item.sortValue);
				return item
				
			})
			this.$emit('sort',{key:key,value:value})
		},
		groupedProject(data) {
			let grouped = this._.groupBy(data, "projectId");
			let credit = [];
			for (const [key, value] of Object.entries(grouped)) {
				credit.push(value);
			}
			return credit.length;
		},
		
		async editName(id, name) {
			const app = this;
			const form = {
				accountName: name,
			};
			await this.$axios
				.$put(`/api/v1/account/${id}`, form)
				.then((resp) => {
					// console.log(resp);
					app.$toast.success(app.$t('toast.edit.success'))
					setTimeout(app.$toast.clear, 3000);
					
					app.$emit("getAccount");
					// app.dropdowns.account_types = resp;
				})
				.catch((err) => {
					app.$toast.error(app.$t('toast.edit.error'))
					setTimeout(app.$toast.clear, 3000);
					console.log(err);
				});
		},
		
		
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
		},
		
		
		
		deleteUser(id) {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#ef4444",
					title: this.$t("alert.title.warning"),
					text: this.$t("alert.text.warning.delete"),
					showCancelButton: true,
					reverseButtons: true,

					confirmButtonColor: "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$axios
							.$delete(`/api/v1/account/${id}`)
							.then((resp) => {
								// console.log(resp);
								app.$emit("getAccount");
								// app.form = resp;
								app.$swal.fire({
									icon: "success",
									iconColor: "#059669",
									confirmButtonColor: "#059669",
									title: this.$t("alert.title.success.delete"),
									timer: 2000,
									timerProgressBar: true,
								});
							})
							.catch((err) => {
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