<template>
	<section class="pt-2 pb-4">
		<div class="flex items-center justify-between my-10">
			<div class="flex gap-4 items-center">
				<div class="w-12 h-12 bg-carbon-blue-logo rounded flex items-center justify-center">
					<p class="text-white text-lg">{{ NameProfile(accountName) }}</p>
				</div>
				<div>
					<p class="font-medium capitalize">
						{{ accountName }} <span v-if="account_status === 0" class="text-yellow-500">({{ $t("home.account.pending_status") }})</span>
					</p>
					<div class="flex items-center gap-2 text-sm text-gray-500">
						<p class="capitalize">{{ $t("home.title.account_number") }}:</p>
						<div class="flex items-center relative w-32">
							<input class="w-full outline-none cursor-pointer bg-transparent" readonly @focus="$event.target.select()" ref="clone" :title="$t('click_copy')" id="myToken" @click="copyToClipboard" v-model="accountNumber" />
							<svg @click="copyToClipboard" :title="$t('click_copy')" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 absolute z-10 top-0 right-0 cursor-pointer">
								<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 01-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 011.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 00-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 01-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 00-3.375-3.375h-1.5a1.125 1.125 0 01-1.125-1.125v-1.5a3.375 3.375 0 00-3.375-3.375H9.75" />
							</svg>
						</div>
					</div>
				</div>
			</div>
			<div class="flex items-center gap-4">
				<div class="">
					<button :disabled="checkDisable" @click="_openTokenModal()" :class="{ 'bg-gray-300 text-gray-400 cursor-not-allowed': checkDisable, 'bg-gray-800 hover:bg-gray-700 text-white': !checkDisable }" class="px-5 py-2 text-sm rounded shadow-sm">{{ $t("button.get_account_token") }}</button>
				</div>
				<!-- <div class="">
					<a :href="localePath(`/profile`)" class="px-5 py-2 text-sm bg-carbon-blue-logo hover:bg-tgo-teal-600 text-white rounded shadow-sm">{{ $t("button.edit_profile") }}</a>
				</div> -->
			</div>
		</div>

		<HomeTokenModal v-show="openTokenModal" @close="openTokenModal = false" :open="openTokenModal"></HomeTokenModal>
		<HomeExportTransactionModal v-show="openExportModal" @close="openExportModal = false"></HomeExportTransactionModal>

		<div class="flex border-b border-gray-300 text-sm">
			<div @click="step = 1" class="px-4 py-1 cursor-pointer" :class="{ ' border-b-2 border-carbon-blue-logo': step === 1 }">{{ $t("home.title.credit_list") }}</div>
			<div @click="step = 2" class="px-4 py-1 cursor-pointer" :class="{ 'border-b-2 border-carbon-blue-logo': step === 2 }">{{ $t("home.title.transaction_history") }}</div>
		</div>

		<div v-if="step == 1" class="w-full mt-4">
			<section class="flex items-center justify-between my-10">
				<div class="flex items-center gap-2">
					<select v-model="limit" @change="getCredit()" class="text-sm text-center border-2 border-tgo-teal-400 px-2 py-0.5 bg-white">
						<option :value="10">10</option>
						<option :value="50">50</option>
						<option :value="100">100</option>
						<option :value="200">200</option>
					</select>
					<div class="w-40 border-2 border-tgo-teal-400">
						<DatePicker @change="getCredit()" :placeholder="$t('credit.table.header.vintage_year')" type="year" v-model="vintage_year" format="DD MMM YYYY" :formatter="yearFormat" value-type="date" :lang="$i18n.locale" input-class="text-center text-sm px-2 py-1 w-full outline-none"></DatePicker>
					</div>
					<div class="flex items-center w-52 text-sm">
						<input @change="getCredit()" v-model="min" :placeholder="$t('credit.min')" class="px-2 py-1 border-2 border-r-0 border-tgo-teal-400 text-center outline-none w-24" />
						<div class="border-t-2 border-b-2 border-tgo-teal-400 bg-tgo-teal-400 py-1 text-center w-4 text-white">-</div>
						<input @change="getCredit()" v-model="max" :placeholder="$t('credit.max')" class="px-2 py-1 border-2 border-l-0 border-tgo-teal-400 text-center outline-none w-24" />
					</div>
				</div>

				<div>
					<div class="flex items-center relative">
						<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						</span>
						<input type="text" v-model="search" @change="getCredit()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1 pl-10 pr-4 border-2 border-tgo-teal-400 outline-none" />
					</div>
				</div>
			</section>

			<HomeCreditTable :project="project" @reload="reloadData" :accountNumber="accountNumber"></HomeCreditTable>

			<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
		</div>

		<div v-if="step == 2" class="w-full mt-4">
			<div class="flex justify-between items-center my-10">
				<div class="flex items-center gap-2">
					<div class="w-72 border-2 rounded border-tgo-teal-500">
						<DatePicker @change="getCredit()" range :placeholder="$t('home.modal.filter.placeholder')" type="date" v-model="vintage_year" format="DD MMM YYYY" :formatter="thaiformatter" value-type="date" :lang="$i18n.locale" input-class="text-center text-sm px-3 py-2 w-full outline-none"></DatePicker>
					</div>
					<button :disabled="transaction.length === 0" @click="openExportStatement()" :class="{ 'bg-gray-200 text-gray-400 cursor-not-allowed': transaction.length === 0, 'bg-tgo-teal-500 hover:bg-tgo-teal-600 text-white': transaction.length > 0 }" class="px-3 py-1.5 rounded shadow flex items-center gap-2 text-sm">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m.75 12l3 3m0 0l3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
						</svg>

						{{ $t("button.export_statement") }}
					</button>
				</div>

				<div class="flex items-center gap-2">
					<div class="flex items-center relative">
						<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 top-2.5">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						</span>
						<input type="text" v-model="transaction_filter.search" @change="getTransaction()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-2 pl-10 pr-4 border-2 rounded border-tgo-teal-500 outline-none" />
					</div>
					<select v-model="transaction_filter.limit" @change="getTransaction()" class="text-sm text-center border-2 rounded border-tgo-teal-500 px-2 py-2 bg-white">
						<option :value="10">10</option>
						<option :value="50">50</option>
						<option :value="100">100</option>
						<option :value="200">200</option>
					</select>
				</div>
			</div>

			<HomeTransactionTable :transaction="transaction"></HomeTransactionTable>
			<PaginationBar :meta="transaction_meta" @loadRequestByPage="changeTransactionPage" />
		</div>
		<loadingCarbon v-if="isLoading"></loadingCarbon>
	</section>
</template>

<script>
	import thaiformatter from "../../mixins/thaiformatter";
	export default {
		name: "CreditManagement",
		layout: "MainLayout",
		middleware: ["auth"],
		mixins: [thaiformatter],

		data() {
			return {
				step: 1,
				isLoading: true,
				refreshData: false,
				openTokenModal: false,
				openExportModal: false,

				min: null,
				max: null,
				limit: 10,
				vintage_year: null,
				search: "",

				meta: {
					pages: 1,
					current_page: 1,
					total: 1,
				},
				stat: {
					total: 0,
					verified: 0,
					pending: 0,
					finish: 0,
				},
				sort: -1,
				sort_by: "registration_date",

				project: [],
				accountNumber: "",
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
				selectInfo: null,
				modalOpen: false,
				accountName: "",
				account_status: null,
			};
		},
		computed:{
			checkDisable(){
				if(this.account_status === 0) return true
				else if(this.$auth.user.appSyncedId.length > 0) return true
				else return false
			}
		},
		watch: {
			status() {
				this.sub_status = "";
			},
		},
		async mounted() {
			if(this.$auth.user.accountID === null){
				this.$router.push(this.localePath('/'))
			}
			await this.getCredit();
			await this.getTransaction();
			this.isLoading = false;
		},
		methods: {
			_openTokenModal() {
				if (this.account_status === 0) {
					return;
				}

				this.openTokenModal = true;
			},
			openExportStatement() {
				if (this.transaction.lenght === 0) {
					return;
				}
				this.openExportModal = true;
			},
			reloadData() {
				this.modalOpen = false;
				this.getCredit();
			},
			NameProfile(aname) {
				return `${aname[0] ?? ""}`;
			},
			changeTransactionPage(page) {
				this.getTransaction(page);
			},
			openModalEvt(data) {
				this.selectInfo = data;
				this.modalOpen = true;
			},
			getTransaction(page = 1) {
				const app = this;
				app.isLoading = true;
				this.transaction_current_page = page;
				this.$axios
					.$get(`/api/v1/credit/transaction?limit=${this.transaction_filter.limit}&page=${this.transaction_current_page}&search=${this.transaction_filter.search}`)
					.then((resp) => {
						app.transaction = resp.data;
						app.transaction_meta = resp.meta;
						app.isLoading = false;
					})
					.catch(() => {
						app.$toast.error(app.$t("toast.loading.error"));
						setTimeout(app.$toast.clear, 3000);
						app.isLoading = false;
					});
			},

			async getCredit(page = 1) {
				const app = this;
				app.isLoading = true;
				this.current_page = page;
				let yearVintage = "";
				if (this.vintage_year !== null) {
					yearVintage = this.$dayjs(this.vintage_year).format("YYYY");
				}
				await this.$axios
					.$get(`/api/v1/credit/table?limit=${this.limit}&page=${this.current_page}&year=${yearVintage}&min=${this.min}&max=${this.max}&search=${this.search}`)
					.then((resp) => {
						// console.log(resp);
						app.project = resp.data;
						app.accountNumber = resp.desAccountNumber;
						app.accountName = resp.accountName;
						app.meta = resp.meta;
						app.account_status = resp.status;
						// this.$toast.success("เพิ่มข้อมูลสำเร็จ");
						// this.$router.push("/users/userManagement");
						// setTimeout(this.$toast.clear, 3000);
						app.isLoading = false;
					})
					.catch((errors) => {
						console.log(errors);
						// this.$toast.error(errors.response.data.errors);
						// setTimeout(this.$toast.clear, 3000);
						app.isLoading = false;
					});
			},
			copyToClipboard() {
				const copyText = document.getElementById("myToken");
				this.$refs.clone.focus();
				try {
					document.execCommand("copy");
					this.$toast.success(this.$t("toast.copy.success"));
				} catch (error) {
					this.$toast.error(this.$t("toast.copy.fail"));
				}

				setTimeout(this.$toast.clear, 3000);
			},

			async loadRequestByPage(pageNumber) {
				await this.getCredit(pageNumber);
			},
		},
	};
</script>

<style>
	.mx-datepicker {
		position: relative;
		display: inline-block;
		width: 100% !important;
	}
</style>
