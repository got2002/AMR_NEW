<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 2xl:overflow-hidden overflow-x-scroll shadow-sm rounded">
		<table class="items-center w-full space-y-6">
			<thead>
				<tr >
					<template v-for="(item, idx) in table.headers">
						<LogHeaderSlot :text="item.name" :key="idx" :align="item.align" />
					</template>
				</tr>
			</thead>
			<tbody class="bg-theme-white">
				<template v-for="(log, index) in logs">
					<tr :key="index" :class="{ 'bg-gray-100 hover:bg-gray-300': index % 2 == 1 }" class="focus:outline-none text-xs hover:bg-gray-50 h-10 rounded align-middle cursor-pointer">
						<td class=" px-1 align-center whitespace-nowrap justify-center text-center">
							<div class="flex items-center justify-center text-xs gap-1">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>

								<span>{{ datetime(log.datetime) }}</span>
							</div>
						</td>
						<td class=" px-1 align-center whitespace-nowrap justify-center text-center">
							<span>{{ log.username || $t('undefined') }}</span>
						</td>
						<td class=" px-1 align-center whitespace-nowrap justify-center text-center">
							<p class="font-bold">{{ log.method }}</p>
						</td>
						<td class=" px-1 align-center whitespace-nowrap justify-center text-center">
							<div class="flex items-center justify-start gap-1">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
									<path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
								</svg>

								<p class="truncate">{{ log.url }}</p>
							</div>
						</td>
						<td class=" px-1 align-center whitespace-nowrap flex items-center justify-center">
							<div class="flex items-center justify-start gap-1 h-10">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
								</svg>

								<span>{{ log.ip }}</span>
							</div>
						</td>
					</tr>
				</template>
			</tbody>
		</table>
		<div v-if="logs.length == 0" class="focus:outline-none text-xs h-16 bg-white rounded hover:bg-theme-green-100 align-middle cursor-pointer">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["logs"],
		data() {
			return {
				table: {
					headers: [
						{
							name: this.$t("log.table.header.log_date"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("log.table.header.username"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("log.table.header.method"),
							align: "center",
							filterable: false,
						},

						{
							name: this.$t("log.table.header.referer"),
							align: "left",
							filterable: false,
						},

						{
							name: "IP",
							align: "center",
							filterable: false,
						},
					],
				},
			};
		},

		mounted() {
			// console.log(this.loggedInUser, this.isAuthenticated)
		},
		methods: {
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
		},
	};
</script>
