<template>
	<div class="w-full overflow-x-auto bg-tgo-teal-500 shadow-sm rounded">
		<table class="items-center w-full space-y-6">
			<thead>
				<tr>
					<template v-for="(header, idx) in data.headers">
						<OrganizationHeaderSlot :key="idx" :header="header"></OrganizationHeaderSlot>
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in data.data">
					<tr :key="index" :class="{ 'bg-gray-100 hover:bg-gray-200': index % 2 == 1 }" class="focus:outline-none text-xs hover:bg-gray-50 h-10 rounded align-middle">
						<OrganizationDataSlot :text="`${data.companyId}`"></OrganizationDataSlot>
						<OrganizationDataSlot :text="getOrganizationName(data.companyName)"></OrganizationDataSlot>
						<OrganizationDataSlot :text="data.fieldOfIndustry"></OrganizationDataSlot>
						<OrganizationDataSlot :text="`${data.companyMembers}`"></OrganizationDataSlot>
						<OrganizationActionSlot :id="data._id" @reload="$emit('reload')"></OrganizationActionSlot>
					</tr>
				</template>
			</tbody>
		</table>

		<div v-if="data.data.length == 0" tabindex="0" colspan="9" class="focus:outline-none text-xs h-16 bg-white rounded hover:bg-theme-green-100 align-middle cursor-pointer">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
	import moment from "moment";

	export default {
	
		props: ["data"],
		data() {
			return {
				sort: [0, 0, -1, 0],
				modalOpen: false,
				
				selectInfo: {},
			};
		},
		computed: {
			// fullName() {
			// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
			// },
		},
		mounted() {
			// console.log(this.loggedInUser, this.isAuthenticated)
		},
		methods: {
			getOrganizationName(organization) {
				if (this.$i18n.locale === "th") {
					return organization.th
				}
				return organization.en
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
							return "รอรับรอง";
						default:
							return "null";
					}
				} else {
					switch (data) {
						case "Registered":
							return "Registered";
						case "Certified":
							return "Certified";
						case "Pending":
							return "Pending";
						case "Cancelled":
							return "Cancelled";
						case "Expired":
							return "Expired";
						default:
							return "null";
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
			statusText(data) {
				if (data === "Pending") {
					return this.$t("project.table.status.pending");
				} else if (data === "Rejected") {
					return this.$t("project.table.status.rejected");
				} else if (data === "Verified") {
					return this.$t("project.table.status.verified");
				} else {
					return this.$t("project.table.status.expired");
				}
			},
		
			setSortValue(text, value) {
				switch (text) {
					case "project_id":
						if (this.sort[0] === 0) {
							this.sort[0] = 1;
						} else if (this.sort[0] === 1) {
							this.sort[0] = -1;
						} else {
							this.sort[0] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 0) {
								this.sort[i] = 0;
							}
						}
						break;
					case "project_name.thai":
						if (this.sort[1] === 0) {
							this.sort[1] = 1;
						} else if (this.sort[1] === 1) {
							this.sort[1] = -1;
						} else {
							this.sort[1] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 1) {
								this.sort[i] = 0;
							}
						}
						break;
					case "project_name.english":
						if (this.sort[1] === 0) {
							this.sort[1] = 1;
						} else if (this.sort[1] === 1) {
							this.sort[1] = -1;
						} else {
							this.sort[1] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 1) {
								this.sort[i] = 0;
							}
						}
						break;
					case "registration_date":
						if (this.sort[2] === 0) {
							this.sort[2] = 1;
						} else if (this.sort[2] === 1) {
							this.sort[2] = -1;
						} else {
							this.sort[2] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 2) {
								this.sort[i] = 0;
							}
						}
						break;
					case "carbon_credit_total":
						if (this.sort[3] === 0) {
							this.sort[3] = 1;
						} else if (this.sort[3] === 1) {
							this.sort[3] = -1;
						} else {
							this.sort[3] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 3) {
								this.sort[i] = 0;
							}
						}
						break;
					default: {
						if (this.sort[0] === 0) {
							this.sort[0] = 1;
						} else if (this.sort[0] === 1) {
							this.sort[0] = -1;
						} else {
							this.sort[0] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 0) {
								this.sort[i] = 0;
							}
						}
						break;
					}
				}
				this.$emit("searchKeyup", text, this.sort[value]);
			},
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
		},
	};
</script>
<style>
	.table-mim-w {
		min-width: 100%;
	}
</style>
