<template>
	<div class="w-full space-y-4">
		<div>
			<button @click="$router.push(localePath('/showroom'))" class="px-4 py-2 flex items-center gap-2 bg-gray-300 rounded shadow-md text-sm">
				<ShowroomBackIcon />
				{{ $t("button.back") }}
			</button>
		</div>
		<div class="grid grid-cols-12 gap-4">
			<div class="col-span-3">
				<div class="grid grid-cols-4 gap-4">
					<div class=" bg-white rounded col-span-4 shadow-md">
						<img v-if="info.project_picture?.length>0" :src="imgPreview" class="w-full h-80 object-cover rounded" />
						<img v-else src="https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80" class="w-full h-80 object-cover rounded" />
					</div>

					<template v-for="(img, i) in info.project_picture">
						<div @click="previewImg(i)" :key="i" class="bg-white rounded col-span-1" :class="{'shadow-md':imgPreview === imgUrl(img.src)}">
							<img :src="imgUrl(img.src)" class="h-20 w-20 object-cover rounded" />
						</div>
					</template>

					<div class="col-span-4">
						<UILabel :text="$t('project.view_page.project_developer')" class="font-bold" />
						<p class="text-gray-500 text-sm break-words">{{ projectDevelopertext(info) }}</p>
					</div>
					<div class="col-span-4">
						<UILabel :text="$t('project.view_page.project_owner')" class="font-bold" />
						<p class="text-gray-500 text-sm">{{ projectOwnertext(info) }}</p>
					</div>
					<div class="col-span-4">
						<UILabel :text="$t('project.view_page.registered_date')" class="font-bold" />
						<p class="text-gray-500 text-sm">{{ dateFormat(info.registration_date) }}</p>
					</div>
					<div class="col-span-4">
						<UILabel :text="$t('project.view_page.credit_period_project')" class="font-bold" />
						<p class="text-gray-500 text-sm">{{ dateFormat(info.valid_start) }} - {{ dateFormat(info.valid_end) }}</p>
					</div>
				</div>
			</div>
			<div class="col-span-9">
				<div>
					<p class="text-xl font-semibold">{{ projectName(info.project_name) }}</p>
					<p class="text-gray-500 text-base">{{ $t("showroom.vintage_card.total_availability") }} {{totalAvailable?.toLocaleString()}} tCO<sub>2</sub>e</p>
				</div>
				<div class="w-full h-0.5 bg-gray-300 my-4"></div>
				<div>
					<p class="text-sm font-semibold">{{ $t("project.view_page.project_overview") }}</p>
					<p class="font-thin text-sm">{{ projectActivityLang(info) }}</p>
				</div>

				<div class="w-full h-0.5 bg-gray-300 my-4"></div>
				<div class="space-y-2 text-sm">
					<p>
						<span class="font-semibold">{{ $t("project.view_page.knp_rule") }}:</span> <span class="font-thin">{{ ccmgm(info.project_type_by_extens) }}</span>
					</p>
					<p>
						<span class="font-semibold">{{ $t("project.view_page.standard") }}:</span> <span class="font-thin">{{ info.standard }}</span>
					</p>
					<p>
						<span class="font-semibold">{{ $t("project.view_page.programid") }}:</span> <span class="font-thin">{{ info.programID }}</span>
					</p>
					<p>
						<span class="font-semibold">{{ $t("project.view_page.authorizeduse") }}:</span> <span class="font-thin">{{ getAuthorizedUseText(info.authorizedUse) }}</span>
					</p>
				</div>

				<div class="w-full h-0.5 bg-gray-300 my-4"></div>
				<ShowroomCoBenefit :form="info" />
				<div class="w-full h-0.5 bg-gray-300 my-4"></div>
				<div class="grid grid-cols-12 gap-4">
					<!-- <ShowroomVintageCard v-for="i in 1" :key="i"/>
                    <ShowroomVintageCard2 v-for="i in 1" :key="i"/> -->

					<ShowroomVintageCard v-for="item in showroom" :key="item._id" :info="item" :cart="cart" :projectInfo="info"/>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "ShowroomCO2Info",
	layout: "MainLayout",
	data() {
		return {
			cart: [],
			info: {},
			dropdowns: {
				autherizeduses: [],
			},
			showroom: [],
			imgPreview: "",
			
		};
	},
	computed:{
		totalAvailable(){
			return this._.sumBy(this.showroom,(item)=>item.available)
		}
	},
	async mounted() {
		// this.cart = this.$auth.$storage.getLocalStorage("cart");
		await this.getDropdownAutherizedUse();
		await this.getProject();
		await this.getShowroom();
	},
	methods: {
		imgUrl(url) {
			if (url?.length !== null) {
				return process.env.baseUrl + url;
			} else return "https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80";
		},
		async getDropdownAutherizedUse() {
			const app = this;
			await this.$axios
				.$get(`/api/v1/dropdown/authorizeduses`)
				.then((resp) => {
					// console.log(resp);
					app.dropdowns.autherizeduses = resp;
				})
				.catch((errors) => {
					console.log(errors);
				});
		},
		getAuthorizedUseText(value) {
			return this._.find(this.dropdowns.autherizeduses, (item) => item.value === value)?.text;
		},
		projectDevelopertext(data) {
			if (this.$i18n.locale === "th") return data.project_developer;
			else return data.project_developer_en;
		},
		projectOwnertext(data) {
			if (this.$i18n.locale === "th") return data.project_owner;
			else return data.project_owner_en;
		},
		dateFormat(date) {
			if (this.$i18n.locale === "th") return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			else return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		projectName(name) {
			if (this.$i18n.locale === "th") return name?.thai;
			else return name?.english;
		},
		projectActivityLang(data) {
			if (this.$i18n.locale === "th") {
				return data?.project_activity;
			}
			return data?.project_activity_en;
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
		getProject() {
			const app = this;
			this.$axios.$get(`/api/v1/home/${this.$route.params.id}`).then((resp) => {
				app.info = resp;
				app.previewImg(0)
			});
		},
		previewImg(i) {
			this.imgPreview = this.imgUrl(this.info?.project_picture[i]?.src);
		},
		getShowroom() {
			const app = this;
			this.$axios.$get(`/api/v1/showroom/available-tonnes/${this.$route.params.id}`).then((resp) => {
				app.showroom = resp;
			});
		},
	},
};
</script>

<style>
</style>