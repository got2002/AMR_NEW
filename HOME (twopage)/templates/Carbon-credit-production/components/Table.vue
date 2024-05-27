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
					<tr tabindex="0" :class="{ 'bg-gray-100': index % 2 == 1 }" class="focus:outline-none text-xs h-10 rounded hover:bg-theme-green-100 align-middle cursor-pointer" @click="Onpage(data._id)" :key="index">
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-left">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">#{{ data.project_id }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-start projectname" @mouseover="mousePosition">
							<div :style="`top:${y}px;left:${x}px`" :class="`rounded-sm absolute z-50 px-4 py-2 bg-white text-sm border border-gray-500`" tooltip>{{ projectName(data.project_name) }}</div>
							<div class="lg:w-60 md:w-52 w-40 h-auto break-all">
								<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate text-left">{{ projectName(data.project_name) }}</p>
							</div>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-start ccmgm" @mouseover="mousePosition">
							<div :style="`top:${y}px;left:${x}px`" :class="`rounded-sm absolute z-50 px-4 py-2 bg-white text-sm border border-gray-500`" tooltip>{{ ccmgm(data.project_type_by_extens) }}</div>

							<div class="w-60 h-auto break-all">
								<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate text-left">{{ ccmgm(data.project_type_by_extens) }}</p>
							</div>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate">{{ data.standard || $t("alert.undefined") }}</p>
						</td>

						<!--  <td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ data.approx_co2_reduction_per_year }} {{ $t("project.view_page.ton") }}</span>
						</td> -->
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ datetime(data.registration_date) }}</span>
						</td>

						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ datetime(data.valid_start) }} - {{ datetime(data.valid_end) }}</span>
						</td>

						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ data.carbon_credit_total.toLocaleString() }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap text-center">
							<span
								class="font-medium text-xs leading-6 ml-2"
								:class="{
									'text-green-500': data.status == 'Registered',
									'text-red-500': data.status == 'Cancelled',
									'text-gray-500': data.status == 'Expired',
								}"
								>{{ statustran(data.status) }}</span
							>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap text-center">
							<span
								class="font-medium text-xs leading-6 ml-2"
								:class="{
									'text-yellow-600': data.sub_status == 'Pending',
									'text-green-500': data.sub_status == 'Certified',
								}"
								>{{ statustran(data.sub_status) }}</span
							>
						</td>

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
						name: this.$t("project.table.header.project_id"),
						align: "left",
						sortable: true,
						sortValue: -1,

						sortKey: "project_id",
					},
					{
						name: this.$t("project.table.header.project_title"),
						align: "left",
						sortable: true,
						sortValue: 0,

						sortKey: this.$i18n.locale === "th" ? "project_name.thai" : "project_name.english",
					},
					{
						name: this.$t("project.table.header.project_type"),
						align: "center",
						sortable: false,
						sortValue: 0,

						sortKey: "project_type",
					},

					{
						name: this.$t("project.table.header.standard"),
						align: "center",
						sortable: false,
						sortValue: 0,

						sortKey: "project_id",
					},

					{
						name: this.$t("project.table.header.registered"),
						align: "center",
						sortable: true,
						sortValue: -1,

						sortKey: "registration_date",
					},
					{
						name: this.$t("project.table.header.credit_period_project"),
						align: "center",
						sortable: false,
						sortValue: 0,

						sortKey: "credit_period_project",
					},

					{
						name: this.$t("project.table.header.co2_amount"),
						align: "center",
						sortable: true,
						sortValue: 0,

						sortKey: "carbon_credit_total",
					},
					{
						name: this.$t("project.table.header.status"),
						align: "center",
						sortable: false,
						sortValue: 0,

						sortKey: "project_id",
					},
					{
						name: this.$t("project.table.header.sub_status"),
						align: "center",
						sortable: false,
						sortValue: 0,

						sortKey: "project_id",
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
			this.x = e.pageX + 10;
			this.y = e.pageY;
		},
		ccmgm(data) {
			if (this.$i18n.locale === "th") {
				return data;
			} else {
				switch (data) {
					case "พลังงานหมุนเวียนหรือพลังงานที่ใช้ทดแทนเชื้อเพลิงฟอสซิล":
						return "Renewable energy or fossil fuel replacement";
					case "การเพิ่มประสิทธิภาพการผลิตไฟฟ้าและการผลิตความร้อน":
						return "Improvement of the efficiency of electricity and heat generation";
					case "การใช้ระบบขนส่งสาธารณะ":
						return "Use of public transportation system";
					case "การใช้ยานพาหนะไฟฟ้า":
						return "Use of electric vehicle";
					case "การเพิ่มประสิทธิภาพเครื่องยนต์":
						return "Improvement of the efficiency of engine";
					case "การเพิ่มประสิทธิภาพการใช้พลังงานในอาคารและโรงงาน และในครัวเรือน":
						return "Improvement of the efficiency of energy consumption in building and factory and in household";
					case "การปรับเปลี่ยนสารทำความเย็นธรรมชาติ":
						return "Use of natural refrigerant";
					case "การใช้วัสดุทดแทนปูนเม็ด":
						return "Use of clinker substitute";
					case "การจัดการขยะมูลฝอย":
						return "Solid waste management";
					case "การจัดการน้ำเสียชุมชน":
						return "Domestic wastewater management";
					case "การนำก๊าซมีเทนกลับมาใช้ประโยชน์":
						return "Methane recovery and utilization";
					case "การจัดการน้ำเสียอุตสาหกรรม":
						return "Industrial wastewater management";
					case "การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร":
						return "Reduction, absorption and removal of greenhouse gases from the forestry and agriculture sectors";
					case "การดักจับ กักเก็บ และ/หรือใช้ประโยชน์จากก๊าซเรือนกระจก":
						return "Capture, storage, and/or utilization of greenhouse gas";
					default:
						return "Other project specified by the Board of Directors of TGO";
				}
			}
		},
		projectName(data) {
			if (this.$i18n.locale === "th") {
				return data.thai;
			} else {
				return data.english;
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
