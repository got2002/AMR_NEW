<template>
	<section class="pt-2 pb-4">
		<div class="flex flex-col items-start">
			<div>
				<h2 class="text-3xl font-bold">{{ $t("account.page_title") }}</h2>
				<div v-if="step == 1" class="mb-1 text-sm font-normal opacity-50">{{ $t("show_data", { from: meta.current_page * 10 - 9, to: meta.current_page * 10 - (10 - accounts.length), all: meta.total }) }}</div>
				<div v-else-if="step == 2" class="mb-1 text-sm font-normal opacity-50">{{ $t("show_data", { from: pending_accounts_meta.current_page * 10 - 9, to: pending_accounts_meta.current_page * 10 - (10 - accounts.length), all: pending_accounts_meta.total }) }}</div>
			</div>

			<section class="flex items-center justify-between mt-6 mb-4 w-full">
				<div class="flex items-end gap-2">
					<div class="">
						<select v-if="step == 1" v-model="limit" @change="getAccount()" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
						<select v-else-if="step == 2" v-model="limit" @change="getPendingAccount()" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
					</div>

					<div class="relative">
						<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 px-2 py-1.5">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						</span>
						<input @change="getAccount()" v-model="search" type="text" :placeholder="$t('user.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-200 rounded outline-none" />
					</div>
				</div>
				<div>
					<nuxt-link :to="localePath({ name: 'accounts-create' })" class="px-2 py-1 bg-tgo-teal-500 hover:bg-tgo-teal-600 hover:text-theme-white shadow-sm rounded text-white flex items-center">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
						</svg>

						{{ $t("account.filter.addAccount") }}</nuxt-link
					>
				</div>
			</section>
			<div class="flex border-b border-gray-300 text-sm my-5">
				<div @click="step = 1" class="px-4 py-1 cursor-pointer" :class="{ ' border-b-2 border-carbon-blue-logo': step === 1 }">{{ $t("home.title.account_list") }}</div>
				<div @click="step = 2" class="px-4 py-1 cursor-pointer relative flex items-center gap-2" :class="{ 'border-b-2 border-carbon-blue-logo': step === 2 }">
					{{ $t("home.title.new_account") }}
					<div v-if="pending_accounts_meta?.total > 0" class="bg-tgo-teal-500 text-white text-sm w-5 h-5 flex items-center justify-center rounded-full">{{ pending_accounts_meta.total }}</div>
				</div>
			</div>
			<div v-if="step == 1" class="w-full">
				<!-- <template v-for="(acc, idx) in accounts">
					<AccountCard @reload="getAccount()" :key="idx" :index="idx" :data="acc"></AccountCard>
				</template> -->
				<AccountTable :tHead="table.head" :tData="accounts" @getAccount="getAccount(1)" @sort="getAccount(1,$event)"/>
				<div v-if="accounts.length == 0" class="2xl:col-span-5 lg:col-span-3 md:col-span-2 bg-white h-20 flex items-center justify-center border">
					{{ $t("no_data") }}
				</div>
			</div>
			<div v-if="step == 2" class="w-full">
				<AccountApproveTable :tData="pending_accounts" @reload="getPendingAccount()" />
				<div v-if="pending_accounts.length == 0" class="2xl:col-span-5 lg:col-span-3 md:col-span-2 bg-white h-20 flex items-center justify-center border">
					{{ $t("no_data") }}
				</div>
			</div>
		</div>
		<PaginationBar v-if="step == 1" :meta="meta" @loadRequestByPage="loadRequestByPage" />
		<PaginationBar v-if="step == 2" :meta="pending_accounts_meta" @loadRequestByPage="getPendingAccount" />
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
			step: 1,
			openFilter: true,
			sortKey:'',
			sortValue:0,
			table: {
				head: [
					{
						name: this.$t("account.table.header.account_id"),
						align: "left",
						sortable:false,
						sortKey:'desAccountNumber',
						sortValue:0,
						
					},
					{
						name: this.$t("account.table.header.name"),
						align: "left",
						sortable:false,
						sortKey:'accountName',
						sortValue:0,

					},
					{
						name: this.$t("account.table.header.number_of_projects"),
						align: "center",
						sortable:true,
						sortKey:'blockProjects',
						sortValue:0,

					},
					{
						name: this.$t("account.table.header.credit"),
						align: "center",
						sortable:true,
						sortKey:'totalCredits',
						sortValue:0,

					},
					{
						name: this.$t("account.table.header.createAt"),
						align: "center",
						sortable:false,
						sortKey:'account_id',
						sortValue:0,

					},
					{
						name: this.$t("account.table.header.tool"),
						align: "center",
						sortable:false,
						sortKey:'account_id',
						sortValue:0,

					},
				],
			},
			current_page: 1,
			limit: 10,
			role: -1,
			status: -1,
			organization: -1,
			search: "",
			dropdowns: {
				organization: [],
			},
			stat: {
				organization: 0,
				pending: 0,
				total: 0,
				verified: 0,
			},
			loading: true,
			accounts: [],
			pending_accounts: [],
			pending_accounts_meta: {
				pages: 1,
				current_page: 1,
				total: 0,
			},
		};
	},
	mounted() {
		this.getOrganization();
		// this.getUsers();
		this.getUserStat();
		this.getAccount();
		this.getPendingAccount();
	},
	methods: {
		async loadRequestByPage(pageNumber) {
			// this.current_page = pageNumber;

			await this.getAccount(pageNumber);
		},

		getAccount(page = 1,sort={key:'totalCredit',value:0}) {
			const app = this;
			this.loading = true;
			this.current_page = page;
			this.$axios.$get(`/api/v1/account?page=${this.current_page}&limit=${this.limit}&search=${this.search}&status=${1}&sortKey=${sort.key}&sortValue=${sort.value}`).then((resp) => {
				app.accounts = resp.data;
				app.meta = resp.meta;
				// console.log(resp.data);
				app.loading = false;
			});
		},
		getPendingAccount(page = 1) {
			const app = this;
			this.loading = true;
			this.current_page = page;
			this.$axios.$get(`/api/v1/account?page=${this.current_page}&limit=${this.limit}&search=${this.search}&status=${0}`).then((resp) => {
				app.pending_accounts = resp.data;
				app.pending_accounts_meta = resp.meta;
				// console.log(resp.data);
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
	},
};
</script>

<style></style>
