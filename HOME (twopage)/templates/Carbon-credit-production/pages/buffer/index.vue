<template>
	<section class="pt-2 pb-4">
		<div class="flex items-center justify-between my-10">
			<div>
				<h2 class="text-2xl font-bold">
					{{ $t("buffer.page_title") }}
					<!-- <span class="text-gray-500">({{ accountName ?? "" }})</span> -->
				</h2>
			</div>
			<div>
				<div class="flex items-center gap-4">
					<!-- <button :disabled="checkDisable" @click="_openTokenModal()" :class="{ 'bg-gray-300 text-gray-400 cursor-not-allowed': checkDisable, 'bg-gray-800 hover:bg-gray-700 text-white': !checkDisable }" class="px-5 py-2 text-sm rounded shadow-sm">{{ $t("button.get_account_token") }}</button> -->
					<nuxt-link :to="localePath('/accounts')" class="px-6 py-2 bg-gray-300 border border-gray-500 rounded shadow-sm hover:bg-gray-400">{{ $t("button.back") }}</nuxt-link>
				</div>
			</div>
		</div>
		<AccountTokenModal v-show="openTokenModal" @close="openTokenModal = false" :open="openTokenModal" :account_id="$route.params.id"></AccountTokenModal>
		<AccountSkeletonLoad v-if="loading"></AccountSkeletonLoad>
		<div v-if="!loading">
			<div class="w-full mt-4">
				<TabWidget :items="[$t('buffer.tab.buffer'), $t('buffer.tab.reversal')]" @tab="tab = $event"></TabWidget>
				<div v-if="tab === 0" class="mt-4">
					<section class="flex items-center justify-between mb-2">
						<div class="flex items-center gap-2">
							<select v-model="buffer.limit" @change="getAccount(1)" class="text-sm text-center border border-gray-300 px-2 py-1 rounded bg-white outline-none">
								<option :value="10">10</option>
								<option :value="50">50</option>
								<option :value="100">100</option>
								<option :value="200">200</option>
							</select>
							<div class="w-40 border border-gray-300">
								<DatePicker @change="getAccount()" :placeholder="$t('credit.table.header.vintage_year')" type="year" v-model="buffer.vintage_year" format="DD MMM YYYY" :formatter="yearFormat" value-type="date" :lang="$i18n.locale" input-class="text-center text-sm px-2 py-1.5 w-full outline-none rounded"></DatePicker>
							</div>
							<div class="flex items-center w-52 text-sm">
								<input @change="getAccount()" v-model="buffer.min" :placeholder="$t('credit.min')" class="px-2 py-1.5 border border-r-0 border-gray-300 text-center outline-none w-24 rounded-l" />
								<div class="border-t border-b border-gray-300 bg-gray-200 py-1.5 text-center w-4">-</div>
								<input @change="getAccount()" v-model="buffer.max" :placeholder="$t('credit.max')" class="px-2 py-1.5 border border-l-0 border-gray-300 text-center outline-none w-24 rounded-r" />
							</div>
						</div>

						<div>
							<div class="flex items-center relative">
								<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
									</svg>
								</span>
								<input type="text" v-model="buffer.search" @change="getAccount()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-300 rounded outline-none" />
							</div>
						</div>
					</section>

					<BufferTable :project="data" @reload="getAccount()" @sort="getAccount(1, $event)" />
					<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
				</div>
				<div v-if="tab === 1" class="mt-4">
					<section class="flex items-center justify-between mb-2">
						<div class="flex items-center gap-2">
							<select v-model="reversal.limit" @change="getReversalRetirement(1)" class="text-sm text-center border border-gray-300 px-2 py-1 rounded bg-white outline-none">
								<option :value="10">10</option>
								<option :value="50">50</option>
								<option :value="100">100</option>
								<option :value="200">200</option>
							</select>
							<div class="w-40 border border-gray-300">
								<DatePicker @change="getReversalRetirement()" :placeholder="$t('credit.table.header.vintage_year')" type="year" v-model="reversal.vintage_year" format="DD MMM YYYY" :formatter="yearFormat" value-type="date" :lang="$i18n.locale" input-class="text-center text-sm px-2 py-1.5 w-full outline-none rounded"></DatePicker>
							</div>
							<div class="flex items-center w-52 text-sm">
								<input @change="getReversalRetirement()" v-model="reversal.min" :placeholder="$t('credit.min')" class="px-2 py-1.5 border border-r-0 border-gray-300 text-center outline-none w-24 rounded-l" />
								<div class="border-t border-b border-gray-300 bg-gray-200 py-1.5 text-center w-4">-</div>
								<input @change="getReversalRetirement()" v-model="reversal.max" :placeholder="$t('credit.max')" class="px-2 py-1.5 border border-l-0 border-gray-300 text-center outline-none w-24 rounded-r" />
							</div>
						</div>

						<div>
							<div class="flex items-center relative">
								<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
									</svg>
								</span>
								<input type="text" v-model="reversal.search" @change="getReversalRetirement()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-300 rounded outline-none" />
							</div>
						</div>
					</section>

					<BufferReversalTable :project="reversal_retirements" @reload="getReversalRetirement()" @sort="getReversalRetirement(1, $event)" />
					<PaginationBar :meta="reversal_retirements_meta" @loadRequestByPage="changeTransactionPage" />
				</div>
			</div>
		</div>
	</section>
</template>

<script>
import thaiformatter from "../../mixins/thaiformatter";
export default {
	mixins: [thaiformatter],
	name: "BufferInfomation",
	layout: "DashboardLayout",
	middleware: ["auth"],
	data() {
		return {
			data: [],
			reversal_retirements: [],
			openExportModal: false,
			openTokenModal: false,
			buffer: {
				min: null,
				max: null,
				limit: 10,
				vintage_year: null,
				search: "",
				current_page: 1,
			},
			reversal: {
				min: null,
				max: null,
				limit: 10,
				vintage_year: null,
				search: "",
				current_page: 1,
			},

			
			meta: {
				pages: 1,
				current_page: 1,
				total: 1,
			},
			reversal_retirements_meta: {
				pages: 1,
				current_page: 1,
				total: 1,
			},

			loading: false,
			tab: 0,
		};
	},
	async mounted() {
		// this.getAccount();
		await this.getAccount();
		await this.getReversalRetirement();
	},
	computed: {
		checkDisable() {
			if (this.appSyncedId.length > 0) return true;
			else return false;
		},
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
		async changeTransactionPage(page) {
			await this.getReversalRetirement(page);
		},

		async getAccount(page = 1, sort = { key: "vintage_year", value: 0 }) {
			this.buffer.current_page = page;
			const app = this;
			let yearVintage = "";
			if (this.buffer.vintage_year !== null) {
				yearVintage = this.$dayjs(this.buffer.vintage_year).format("YYYY");
			}
			app.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("loading"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			app.$swal.showLoading();
			await this.$axios
				.$get(`/api/v1/buffercarbons?page=${this.current_page}&limit=${this.buffer.limit}&sortKey=${sort.key}&sortValue=${sort.value}&vintage_year=${yearVintage}&min_amount=${this.buffer.min}&max_amount=${this.buffer.max}&search=${this.buffer.search}`)
				.then((resp) => {
					app.data = resp.data;

					app.meta = resp.meta;

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
		async getReversalRetirement(page = 1, sort = { key: "vintage_year", value: 0 }) {
			this.reversal.current_page = page;
			const app = this;
			let yearVintage = "";
			if (this.reversal.vintage_year !== null) {
				yearVintage = this.$dayjs(this.reversal.vintage_year).format("YYYY");
			}
			app.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("loading"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			app.$swal.showLoading();
			await this.$axios
				.$get(`/api/v1/buffercarbons/reversal_retirements?page=${this.reversal.current_page}&limit=${this.reversal.limit}&sortKey=${sort.key}&sortValue=${sort.value}&vintage_year=${yearVintage}&min_amount=${this.reversal.min}&max_amount=${this.reversal.max}&search=${this.reversal.search}`)
				.then((resp) => {
					app.reversal_retirements = resp.data;

					app.reversal_retirements_meta = resp.meta;

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

<style>
</style>