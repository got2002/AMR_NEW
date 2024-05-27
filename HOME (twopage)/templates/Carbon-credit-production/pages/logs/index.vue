<template>
	<section class="pt-2 pb-4">
		<div class="flex flex-col items-start">
		
			<h2 class="text-3xl font-bold">{{ $t("log.page_title") }}</h2>
			<div class="mb-1 text-sm font-normal opacity-50">{{ $t("show_data", { from: meta.current_page * 10 - 9, to: meta.current_page * 10 - (10-logs.length), all: meta.total }) }}</div>
		</div>

		<div class="flex flex-row gap-2 items-center my-6">
			<div class="">
				<select @change="getLogs()" v-model="limit" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
					<option :value="10">10</option>
					<option :value="50">50</option>
					<option :value="100">100</option>
				</select>
			</div>
			<div class="border border-gray-200 rounded">
				<DatePicker @change="getLogs()" v-model="period" :format="dateFormat" :lang="$i18n.locale" :range="true" :placeholder="$t('log.filter.period')" input-class="text-center text-sm px-2 py-1.5 w-full outline-none rounded"></DatePicker>
			</div>

			<div class="bg-theme-white">
				<span class="z-10 font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
					</svg>
				</span>
				<input @change="getLogs()" v-model="search" type="text" :placeholder="$t('log.filter.type_to_search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-200 rounded outline-none" />
			</div>
		</div>

		<LogDatatables :logs="logs"></LogDatatables>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
		<loadingCarbon v-if="loading"></loadingCarbon>
	</section>
</template>

<script>
	export default {
		name: "LogPage",
		layout: "DashboardLayout",
		middleware: ["auth"],
		data() {
			return {
				meta: {
					pages: 10,
					current_page: 1,
					total: 100,
				},

				logs: [],
				current_page: 1,
				limit: 10,
				period: [],
				search: "",
				// expandInfo:[],
				toggleExpand: true,

				loading: true,
				dateFormat: "YYYY-MM-DD",
			};
		},
		watch: {
			"$i18n.locale"(locale) {
				if (locale === "th") {
					this.dateFormat = "DD MMM YYYY";
				} else this.dateFormat = "YYYY-MM-DD";
			},
		},
		mounted() {
			this.getLogs();
		},
		methods: {
			loadRequestByPage(page) {
				this.getLogs(page);
			},
			dateTime(date) {
				return this.$moment(date).format("DD MMM YYYY (HH:mm:ss)");
			},
			getLogs(page = 1) {
				const app = this;
				app.loading = true;
				this.current_page = page;
				const startDate = this.period[0] ?? null;
				const endDate = this.period[1] ?? null;
				this.$axios
					.$get(`/api/v1/logging?page=${this.current_page}&limit=${this.limit}&start=${startDate}&end=${endDate}&search=${this.search}`)
					.then((resp) => {
						app.logs = resp.data;
						// app._.forEach(resp.data,item=>{
						// 	app.expandInfo.push(false)
						// })
						app.meta = resp.meta;
						app.loading = false;
					})
					.catch((err) => {
						console.log(err);
						app.loading = false;
					});
			},
		},
	};
</script>

<style>
	.border-gradient {
		border: 2px solid;
		border-image: linear-gradient(to right, #4da366, #1d73c9) 1;
	}
</style>
