<template>
	<section class="pt-2 pb-4">
		<div class="flex items-center justify-between my-10">
			<div>
				<h2 class="text-2xl font-bold">
					{{ $t("account.view.page_title") }} 
					<!-- <span class="text-gray-500">({{ accountName ?? "" }})</span> -->
				</h2>
				<span class="text-sm text-gray-600">{{accountNumber??""}} |</span>
				<span class="text-sm text-gray-600">{{accountName??""}}</span>
				
			</div>
			<div>
				<div class="flex items-center gap-4">
					<button :disabled="checkDisable" @click="_openTokenModal()" :class="{ 'bg-gray-300 text-gray-400 cursor-not-allowed': checkDisable, 'bg-gray-800 hover:bg-gray-700 text-white': !checkDisable }" class="px-5 py-2 text-sm rounded shadow-sm">{{ $t("button.get_account_token") }}</button>
					<nuxt-link :to="localePath('/accounts')" class="px-6 py-2 bg-gray-300 border border-gray-500 rounded shadow-sm hover:bg-gray-400">{{ $t("button.back") }}</nuxt-link>
				</div>
			</div>
			
		</div>
		<AccountTokenModal v-show="openTokenModal" @close="openTokenModal = false" :open="openTokenModal" :account_id="$route.params.id"></AccountTokenModal>
		<AccountSkeletonLoad v-if="loading"></AccountSkeletonLoad>
		<div v-if="!loading">
			<div class="w-full mt-4">
				<section class="flex items-center justify-between mb-2">
					<div class="flex items-center gap-2">
						<select v-model="limit" @change="getAccount(1)" class="text-sm text-center border border-gray-300 px-2 py-1 rounded bg-white outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
						<div class="w-40 border border-gray-300">
							<DatePicker @change="getAccount()" :placeholder="$t('credit.table.header.vintage_year')" type="year" v-model="vintage_year" format="DD MMM YYYY" :formatter="yearFormat" value-type="date" :lang="$i18n.locale" input-class="text-center text-sm px-2 py-1.5 w-full outline-none rounded"></DatePicker>
						</div>
						<div class="flex items-center w-52 text-sm">
							<input @change="getAccount()" v-model="min" :placeholder="$t('credit.min')" class="px-2 py-1.5 border border-r-0 border-gray-300 text-center outline-none w-24 rounded-l" />
							<div class="border-t border-b border-gray-300 bg-gray-200 py-1.5 text-center w-4">-</div>
							<input @change="getAccount()" v-model="max" :placeholder="$t('credit.max')" class="px-2 py-1.5 border border-l-0 border-gray-300 text-center outline-none w-24 rounded-r" />
						</div>
					</div>

					<div>
						<div class="flex items-center relative">
							<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
								</svg>
							</span>
							<input type="text" v-model="search" @change="getAccount()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-300 rounded outline-none" />
						</div>
					</div>
				</section>

				<CreditTable :project="data" :accountNumber="accountNumber" @reload="getAccount()" @sort="getAccount(1,$event)"/>
			</div>
			<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />

			<div class="my-5">
				<div class="flex justify-between items-center mb-2">
					<p class="text-lg font-bold">{{ $t("account.view.transaction") }}</p>
					<div class="flex items-center gap-2">
						<button :disabled="transaction.length === 0" @click="openExportStatement()" :class="{ 'bg-gray-200 text-gray-400 cursor-not-allowed': transaction.length === 0, 'bg-tgo-teal-500 hover:bg-tgo-teal-600 text-white': transaction.length > 0 }" class="px-3 py-1.5 rounded shadow flex items-center gap-2 text-sm">
							<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m.75 12l3 3m0 0l3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
							</svg>

							{{ $t("button.export_statement") }}
						</button>
						<div class="flex items-center relative">
							<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
								</svg>
							</span>
							<input type="text" v-model="transaction_filter.search" @change="getTransaction()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-300 rounded outline-none" />
						</div>
						<select v-model="transaction_filter.limit" @change="getTransaction()" class="text-sm text-center border border-gray-300 px-2 py-1 rounded bg-white outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
					</div>
				</div>
				<AccountTableTransaction :form="transaction"></AccountTableTransaction>
				<PaginationBar :meta="transaction_meta" @loadRequestByPage="changeTransactionPage" />
			</div>
		</div>
		<HomeExportTransactionModal v-show="openExportModal" @close="openExportModal = false" :admin="true"></HomeExportTransactionModal>
	</section>
</template>

<script>
import thaiformatter from "../../../mixins/thaiformatter";
export default {
	name: "DocumentPage",
	layout: "DashboardLayout",
	middleware: ["auth"],
	mixins: [thaiformatter],

	data() {
		return {
			data: [],
			openExportModal: false,
			openTokenModal: false,
			min: null,
			max: null,
			limit: 10,
			vintage_year: null,
			search: "",
			current_page: 1,
			meta: {
				pages: 1,
				current_page: 1,
				total: 1,
			},

			loading: true,
			accountName: "",
			accountNumber: "",
			appSyncedId: [],
			transaction: [],
			transaction_meta: {
				pages: 1,
				current_page: 1,
				total: 1,
			},
			transaction_filter: {
				limit: 10,
				search: "",
			},
		};
	},
	async mounted() {
		// this.getAccount();
		await this.getTransaction();
		await this.getAccount();
	},
	computed:{
		checkDisable(){
			if(this.appSyncedId.length > 0) return true
			else return false
		}
	},
	methods: {
		_openTokenModal() {
			this.openTokenModal = true;
		},
		openExportStatement() {
			if (this.transaction.lenght === 0) {
				return;
			}
			this.openExportModal = true;
		},
		async loadRequestByPage(pageNumber) {
			await this.getAccount(pageNumber);
		},
		changeTransactionPage(page) {
			this.getTransaction(page);
		},
		getTransaction(page = 1) {
			const app = this;

			this.transaction_current_page = page;
			app.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("loading"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			app.$swal.showLoading();
			this.$axios
				.$get(`/api/v1/account/credits/${this.$route.params.id}/transaction?limit=${this.transaction_filter.limit}&page=${this.transaction_current_page}&search=${this.transaction_filter.search}`)
				.then((resp) => {
					app.transaction = resp.data;
					app.transaction_meta = resp.meta;
					app.$swal.close();
				})
				.catch((err) => {
					app.$swal.close();
					console.log(err);
				});
		},
		async getAccount(page = 1,sort={key:'vintage_year',value:0}) {
			this.current_page = page;
			const app = this;
			let yearVintage = "";
			if (this.vintage_year !== null) {
				yearVintage = this.$dayjs(this.vintage_year).format("YYYY");
			}
			app.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("loading"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			app.$swal.showLoading();
			await this.$axios
				.$get(`/api/v1/account/credits/${this.$route.params.id}?limit=${this.limit}&page=${this.current_page}&year=${yearVintage}&min=${this.min}&max=${this.max}&search=${this.search}&sortKey=${sort.key}&sortValue=${sort.value}`)
				.then((resp) => {
					app.data = resp.data;

					app.meta = resp.meta;
					app.accountName = resp.accountName;
					app.accountNumber = resp.desAccountNumber;
					app.appSyncedId = resp.appSyncedId;
					app.$swal.close();
					// console.log(resp);

					// app.getTransaction();
					// app.isData = true;
				})
				.catch((err) => {
					app.$swal.close();
					console.log(err);
				});
			app.loading = false;
		},
		// getTransaction() {
		// 	const app = this;
		// 	this.$axios.$get(`/api/v1/auth/account/transaction?limit=999999`).then((resp) => {
		// 		app.Transaction = resp;
		// 		console.log(resp);
		// 		app.loading = false;
		// 		app.isData = true;
		// 	});
		// },
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM YYYY");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
		},
	},
};
</script>

<style></style>
