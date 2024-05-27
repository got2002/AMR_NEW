<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 2xl:overflow-hidden overflow-x-scroll shadow-sm rounded">
		<table class="items-center w-full space-y-6 shadow-sm rounded-sm">
			<thead>
				<tr>
					<template v-for="(item, idx) in table.head">
						<ApiHeadSlotDark :text="item.name" :key="idx" :align="item.align" />
					</template>
				</tr>
			</thead>
			<tbody class="bg-theme-white">
				<template v-for="(data, index) in dataList">
					<tr :key="index" :class="{ 'bg-gray-100 hover:bg-gray-300': index % 2 == 1 }" class="focus:outline-none text-xs hover:bg-gray-50 h-10 rounded align-middle cursor-pointer">
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ data.name }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ data.email }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span :title="data.scopes.join(', ')" class="px-2 py-1 bg-tgo-teal-500 bg-opacity-10 border border-tgo-teal-500 rounded-full shadow-sm text-tgo-teal-500">{{ data.scopes.length }} {{ $t("api.unit.item") }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ checkstatus(data.status) }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ datetime(data.createdAt) }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ datetime(data.latestLoginAt) }}</span>
						</td>

						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<div class="w-full flex items-center justify-center gap-2">
								<nuxt-link :to="localePath({ name: 'api-id-edit', params: { id: data._id } })">
									<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square text-yellow-500" viewBox="0 0 16 16">
										<path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
										<path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z" />
									</svg>
								</nuxt-link>
								<button @click="deleteApi(data._id)">
									<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash text-red-500" viewBox="0 0 16 16">
										<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
										<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
									</svg>
								</button>
							</div>
						</td>
					</tr>
				</template>
			</tbody>
		</table>
		<div v-if="dataList.length == 0" tabindex="0" colspan="9" class="focus:outline-none text-xs h-16 bg-white rounded hover:bg-theme-green-100 align-middle cursor-pointer">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
	import moment from "moment";
	export default {
		props: ["dataList"],
		data() {
			return {
				table: {
					head: [
						{
							name: this.$t("api.table.header.alias_name"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("api.table.header.email"),
							align: "center",
							filterable: false,
						},

						{
							name: this.$t("api.table.header.permission"),
							align: "center",
							filterable: false,
						},

						{
							name: this.$t("api.table.header.status"),
							align: "center",
							filterable: false,
						},

						{
							name: this.$t("api.table.header.created_date"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("api.table.header.last_used"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("api.table.header.tools"),
							align: "center",
							filterable: false,
						},
					],
				},
				status: [
					{
						text: "Draft",
						value: 0,
					},
					{
						text: "Released",
						value: 1,
					},
					{
						text: "Terminated",
						value: 2,
					},
					{
						text: "Temporary closed",
						value: 3,
					},
				],

				meta: {},

				isLoading: true,
			};
		},
		computed: {
			// fullName() {
			// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
			// },
		},

		methods: {
			dateLocale(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY");
				// return this.$dayjs(date).locale("en").format("DD MMM YYYY");
			},
			datetime(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
				// return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
			},
			checkstatus(value) {
				let status = "";
				this.status.forEach((element) => {
					if (element.value === value) {
						status = element.text;
					}
				});
				return status;
			},

			dateToString(data) {
				return moment(data).format("YYYY-MM-DD");
			},
			fullname(data) {
				return data.firstname + " " + data.lastname;
			},
			sumCarbon(data) {
				let sum = 0;
				data.forEach((element) => {
					sum += element.amount;
				});
				return sum;
			},
			Onpage(id) {
				this.$router.push(this.localePath({ name: "project-id", params: { id: id } }));
			},
			deleteApi(id) {
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
						reverseButtons:true
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
								.$delete(`/api/v1/app/${id}`)
								.then((resp) => {
									// console.log(resp);
									app.$swal.close();

									// app.form = resp;
									app.$swal
										.fire({
											icon: "success",
											iconColor:'#059669',
											confirmButtonColor: "#059669",
											title: this.$t("alert.title.success.delete"),
											timer: 2000,
											// timerProgressBar: true,
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
										timer: 2000,
										// timerProgressBar: true,
									});
									console.log(err);
								});
						}
					});
			},
		},
	};
</script>
