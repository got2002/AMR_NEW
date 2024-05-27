<template>
	<section class="pt-2 pb-4">
		<div class="flex flex-wrap flex-col items-start">
			<h2 class="mb-4 text-3xl font-bold">{{ $t("user.page_title") }}</h2>
			<div class="w-full grid lg:grid-cols-4 grid-cols-2 gap-4">
				<div class="col-span-1">
					<UserCarbonCreditAmount :title="$t('user.statCO2VolumeTitle.all')" :value="stat.total" :icon="1"></UserCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<UserCarbonCreditAmount :title="$t('user.statCO2VolumeTitle.pending')" :value="stat.pending" :icon="4"></UserCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<UserCarbonCreditAmount :title="$t('user.statCO2VolumeTitle.approved')" :value="stat.verified" :icon="3"></UserCarbonCreditAmount>
				</div>

				<div class="col-span-1">
					<UserCarbonCreditAmount :title="$t('user.statCO2VolumeTitle.rejected')" :value="stat.rejected" :icon="2"></UserCarbonCreditAmount>
				</div>
			</div>

			<section class="flex flex-wrap items-center justify-between my-5 w-full">
				<div class="flex flex-wrap items-center gap-2">
					<div class="">
						<select v-model="limit" @change="getUsers()" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
					</div>

					<div class="">
						<select @change="getUsers()" v-model="role" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="-1">{{ $t("user.filter.role.all") }}</option>
							<option :value="0">{{ $t("user.filter.role.user") }}</option>
							<option :value="1">{{ $t("user.filter.role.moderator") }}</option>
							<option :value="99">{{ $t("user.filter.role.admin") }}</option>
						</select>
					</div>
					<div class="">
						<select @change="getUsers()" v-model="status" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="-1">{{ $t("user.filter.status.all") }}</option>
							<option :value="0">{{ $t("user.filter.status.pending") }}</option>
							<option :value="1">{{ $t("user.filter.status.approved") }}</option>
						</select>
					</div>
					<div class="relative">
						<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 px-2 py-1.5">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						</span>
						<input @change="getUsers()" v-model="search" type="text" :placeholder="$t('user.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-200 rounded outline-none" />
					</div>

					<!-- <div :class="{'w-60':organization === '','w-auto':organization}">
						
						<v-select @input="getUsers()" v-model="organization" :placeholder="$t('user.filter.organization')" :options="dropdowns.organization" :reduce="(item) => item.value" :label="$i18n.locale"></v-select>
					</div> -->
				</div>
				<div class="flex items-center gap-2">
					<div>
						<button @click="export_user()" class="px-2 py-1.5 bg-tgo-teal-500 hover:bg-tgo-teal-600 shadow-sm rounded text-white text-sm flex items-center gap-1">
							{{ $t("button.export_user") }}
						</button>
					</div>
					<div>
						<nuxt-link :to="localePath({ name: 'users-create' })" class="px-2 py-1.5 bg-tgo-teal-500 hover:bg-tgo-teal-600 shadow-sm rounded text-white text-sm flex items-center gap-1">
							<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
							</svg>

							{{ $t("button.add_user") }}</nuxt-link
						>
					</div>
				</div>
			</section>

			<UserTable
				:tData="users"
				:tHead="table.head"
				@reload="
					getUsers();
					getUserStat();
				"
				@sort="getUsers(1, $event)"
			/>
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
		<loadingCarbon v-if="loading"></loadingCarbon>
	</section>
</template>

<script>
export default {
	name: "DocumentPage",
	layout: "DashboardLayout",
	middleware: ["auth"],
	data() {
		return {
			meta: {
				pages: 1,
				current_page: 1,
				total: 1,
			},
			openFilter: false,
			table: {
				head: [
					{
						name: this.$t("user.table.header.name"),
						align: "left",
						sortable: false,
						sortKey: "blockProjects",
						sortValue: 0,
					},
					{
						name: this.$t("user.table.header.email"),
						align: "left",
						sortable: false,
						sortKey: "blockProjects",
						sortValue: 0,
					},

					{
						name: this.$t("user.table.header.organization"),
						align: "left",
						sortable: false,
						sortKey: "blockProjects",
						sortValue: 0,
					},

					{
						name: this.$t("user.table.header.role"),
						align: "center",
						sortable: false,
						sortKey: "blockProjects",
						sortValue: 0,
					},

					{
						name: this.$t("user.table.header.status"),
						align: "center",
						sortable: false,
						sortKey: "blockProjects",
						sortValue: 0,
					},

					{
						name: this.$t("user.table.header.registere_date"),
						align: "center",
						sortable: true,
						sortKey: "createdAt",
						sortValue: -1,
					},

					{
						name: this.$t("user.table.header.last_login"),
						align: "center",
						sortable: false,
						sortKey: "blockProjects",
						sortValue: 0,
					},
					{
						name: this.$t("user.table.header.tool"),
						align: "center",
						sortable: false,
						sortKey: "blockProjects",
						sortValue: 0,
					},
				],
			},

			users: [],
			current_page: 1,
			limit: 10,
			role: -1,
			status: -1,
			organization: "",
			search: "",
			dropdowns: {
				organization: [],
			},
			stat: {
				rejected: 0,
				pending: 0,
				total: 0,
				verified: 0,
			},
			loading: true,
		};
	},
	mounted() {
		this.getOrganization();
		this.getUsers();
		this.getUserStat();
	},
	methods: {
		async loadRequestByPage(pageNumber) {
			// console.log(`[Info] - Request Page Number ${pageNumber}`);
			await this.getUsers(pageNumber);
		},
		getUsers(page = 1, sort = { key: "createdAt", value: -1 }) {
			const app = this;
			app.loading = true;
			app.current_page = page;
			this.$axios.$get(`/api/v1/user?page=${this.current_page}&limit=${this.limit}&role=${this.role}&status=${this.status}&search=${this.search}&sortKey=${sort.key}&sortValue=${sort.value}`).then((resp) => {
				app.users = resp.data;
				app.meta = resp.meta;
				app.loading = false;
			});
		},

		getOrganization() {
			const app = this;
			this.$axios.$get(`/api/v1/dropdown/organization`).then((resp) => {
				app.dropdowns.organization = resp;
				app.loading = false;
			});
		},
		getUserStat() {
			const app = this;
			this.$axios.$get(`/api/v1/stats/users`).then((resp) => {
				app.stat = resp;
				app.loading = false;
			});
		},
		export_user(){
			const app = this;
			this.loading = true;
			this.$axios
				.get(`/api/v1/user/export_user_account`)
				.then((res) => {
					// if (res.statusCode === 200) {
						const a = document.createElement('a')
						const universalBOM = "\uFEFF";
						a.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(universalBOM+res.data))
						a.setAttribute(
						'download',
						`${this.$dayjs().format('YYYY_MM_DD')}.csv`
						)
						a.setAttribute('target','_blank')
						a.click()
					// }
				})
				.catch((e)=>{
					this.$toast.error(app.$t("toast.loading.error"));
					setTimeout(this.$toast.clear, 3000);
				})
				.finally(()=>{
					this.loading = false;
				})
		}
	},
};
</script>

<style scoped>
.vs__dropdown-toggle {
	background: #fff;

	border: 2px solid #00b0d8 !important;
	display: flex;
	padding: 1px 0px 1px 40px !important;
}
</style>
