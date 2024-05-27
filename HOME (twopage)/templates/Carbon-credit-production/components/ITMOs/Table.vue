<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 overflow-x-auto rounded shadow-sm">
		<table class="items-center w-full space-y-6 shadow-sm rounded-sm">
			<thead>
				<tr class="bg-tgo-teal-500 text-gray-200 text-sm font-thin">
					
					<TableHeaderSlot v-for="(header,idx) in table.head" :header="header" :key="idx" @setSortValue="setSortValue(header.sortKey, $event)"/>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in project">
					<tr tabindex="0" :class="{ 'bg-gray-100': index % 2 == 1 }" class="focus:outline-none text-xs h-10 rounded hover:bg-theme-green-100 align-middle cursor-pointer" :key="index">
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ datetime(data.transaction_date) }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-left " @click="Onpage(data.project_object_id)">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 hover:text-blue-600 hover:underline hover:cursor-pointer" >#{{ data.project_id }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-start projectname" @mouseover="mousePosition">
							<div :style="`top:${y}px;left:${x}px`" :class="`rounded-sm absolute z-50 px-4 py-2 bg-white text-sm border border-gray-500`" tooltip>{{ projectName(data.project_name) }}</div>
							<div class="lg:w-60 md:w-52 w-40 h-auto break-all">
								<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate text-left">{{ projectName(data.project_name) }}</p>
							</div>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-start ccmgm" @mouseover="mousePosition">
							<div :style="`top:${y}px;left:${x}px`" :class="`rounded-sm absolute z-50 px-4 py-2 bg-white text-sm border border-gray-500`" tooltip>{{ ccmgm(data.project_type) }}</div>

							<div class="w-60 h-auto break-all">
								<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate text-left">{{ ccmgm(data.project_type) }}</p>
							</div>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center">
							<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate">{{ data.serial_number || $t("alert.undefined") }}</p>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ data.total_block.toLocaleString() }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-start text-center cancellationReason" @mouseover="mousePosition">
							<!-- <div :style="`top:${y}px;left:${x}px`" :class="`rounded-sm absolute z-50 px-4 py-2 bg-white text-sm border border-gray-500`" tooltip>{{ cancellationReason(data.reason) }}</div> -->
							<div class="lg:w-60 md:w-52 w-40 h-auto break-all text-center">
								<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate text-center" :title="cancellationReason(data.reason)">{{ cancellationReason(data.reason) }}</p>
							</div>
						</td>

						<!--  <td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ data.approx_co2_reduction_per_year }} {{ $t("project.view_page.ton") }}</span>
						</td> -->
						


						
						

						<!-- <td v-else class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ $t("project.view_page.pending_approval") }}</span>
						</td> -->
					</tr>
				</template>
			</tbody>
		</table>

		<div v-if="project.length == 0" tabindex="0" colspan="9" class="focus:outline-none text-xs h-16 bg-white rounded hover:bg-theme-green-100 align-middle cursor-pointer">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
		<!-- <loadingCarbon v-if="isLoading" /> -->
	</div>
</template>

<script>
import moment from "moment";
export default {
	props: ["project"],
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	data() {
		return {
			type: "",
			status: "",
			province: "",
			min: null,
			isLoading: true,
			max: null,
			searchText: "",
			sortKey:[],
			sortValue:[],
			limit: 10,
			x: 0,
			y: 0,
			table: {
				head: [
					{
						name: this.$t("project.table.header.transaction_date"),
						align: "center",
						sortable: true,
						sortValue: -1,

						sortKey: "transaction_date",
					},
					{
						name: this.$t("project.table.header.project_id"),
						align: "left",
						sortable: true,
						sortValue: -1,

						sortKey: "project_id",
					},
					{
						name: this.$t("project.table.header.project_title"),
						align: "left",
						sortable: false,
						sortValue: 0,

						sortKey: this.$i18n.locale === "th" ? "project_name.th" : "project_name.en",
					},
					{
						name: this.$t("project.table.header.project_type"),
						align: "left",
						sortable: false,
						sortValue: 0,

						sortKey: this.$i18n.locale === "th" ? "project_type.th" : "project_type.en",
					},
					{
						name: this.$t("project.table.header.serial_number"),
						align: "center",
						sortable: true,
						sortValue: 0,

						sortKey: "serial_number",
					},
					{
						name: this.$t("project.table.header.total_block"),
						align: "center",
						sortable: true,
						sortValue: 0,

						sortKey: "total_block",
					},
					{
						name: this.$t("project.table.header.Cooperative Approach"),
						align: "center",
						sortable: false,
						sortValue: -1,

						sortKey: "reason",
					},
					
					
				],
			},
		};
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
	},
	methods: {
		setSortValue(key, value) {
			const findIndex = this._.findIndex(this.sortKey, (item) => item === key);
			if (value === 0) {
				this.sortKey.splice(findIndex, 1);
				this.sortValue.splice(findIndex, 1);
			} else {
				if (findIndex === -1) {
					this.sortKey.push(key);
					this.sortValue.push(value);
				} else this.sortValue[findIndex] = value;
			}

			this.$emit("sort", { key: this.sortKey.join(","), value: this.sortValue.join(",") });
		},
		mousePosition(e){
			// console.log(e);
			this.x = e.pageX + 10
			this.y = e.pageY
		},
		ccmgm(data) {
			if (this.$i18n.locale === "th") {
				return data.th;
			} else {
				return data.en
			}
		},
		projectName(data) {
			if (this.$i18n.locale === "th") {
				return data.th;
			} else {
				return data.en;
			}
		},
		cancellationReason(data) {
			if (this.$i18n.locale === "th") {
				return data.th;
			} else {
				return data.en;
			}
		},
		
		dateLocale(date) {
			// if (this.$i18n.locale === "th") {
			// 	return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			// }
			// return this.$dayjs(date).locale("en").format("DD MMM YYYY");
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},

		statustran(data) {
			if (this.$i18n.locale === "th") {
				switch (data) {
					case "Registered":
						return "ขึ้นทะเบียน";

					case "Cancelled":
						return "ยกเลิก";
					case "Expired":
						return "สิ้นสุดโครงการ";

					case "Certified":
						return "รับรองแล้ว";
					case "Pending":
						return "รอการรับรอง";
					default:
						return "null";
				}
			} else {
				return data;
			}
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
			this.$router.push(this.localePath({ name: "project-id-preview", params: { id: id } }));
		},
	},
};
</script>
<style>
.cancellationReason:hover [tooltip] {
	display: block;
}
</style>
