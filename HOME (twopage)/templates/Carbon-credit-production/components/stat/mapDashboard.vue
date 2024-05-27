<template>
	<div id="map-dashboard" class="rounded-md shadow-lg" style="height: 500px"></div>
</template>

<script>
	export default {
		name: "MapDashboard",
		data() {
			return {
				L: null,
				mapStore: null,
				locations: [],
			};
		},
		async mounted() {
			// const app = this;
			this.L = window.L;
			// console.log(this.L);

			this.mapStore = this.L.map("map-dashboard").setView([13.0, 100.0], 8);
			this.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(this.mapStore);

			await this.getProjectLocations();
			this.drawMarker();
		},
		methods: {
			async getProjectLocations() {
				const app = this;
				await app.$axios
					.$get(`/api/v1/stats/statistics/project-location`)
					.then((resp) => {
						app.locations = resp;
					})
					.catch((err) => err);
			},
			drawMarker() {
				const app = this;
				this._.forEach(this.locations, (item) => {
					// const lat = item.location.geometry.coordinates[1];
					// const lng = item.location.geometry.coordinates[0];
					const projectMarker = app.L.geoJSON(item.location).addTo(app.mapStore);
					projectMarker.on("click", (e) => {
						app.$axios.$get(`/api/v1/project/${item._id}`).then((resp) => {
							console.log(resp);
							app.createPopup(resp, projectMarker);
						});
					});
				});
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
			createPopup(feature, layer) {
				const content = `
				<div class="text-sm font-bold">${this.projectName(feature)}</div>
				<div class="border-t border-gradient my-4"></div>
				<div class="space-y-2">
					<div>${this.$t("project.view_page.project_type")}: <span class="font-semibold">${this.ccmgm(feature.project_type_by_extens)}</span></div>
				
					<div>${this.$t("project.view_page.project_owner")}: <span class="font-semibold">${this.convertLangauge("project_owner", feature)}</span></div>
					
					<div>${this.$t("project.view_page.project_developer")}: <span class="font-semibold">${this.convertLangauge("project_developer", feature)}</span></div>
					<div>${this.$t("project.view_page.registered_date")}: <span class="font-semibold">${this.dateLocale(feature.registration_date)}</span></div>
					<a href="${this.localePath({ name: "project-id", params: { id: feature._id } })}" target="_blank" class="underline text-blue-500 hover:text-blue-600">${this.$i18n.locale === "th" ? "เพิ่มเติม" : "view detail"}</a>
				</div>
				
			`;
				layer.bindPopup(content).openPopup();
			},
			projectName(feature) {
				if (this.$i18n.locale === "th") {
					return feature.project_name.thai;
				}
				return feature.project_name.english;
			},
			convertLangauge(key, feature) {
				if (this.$i18n.locale === "en") {
					return feature[`${key}_en`];
				}
				return feature[`${key}`];
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
		},
	};
</script>

<style>
	.leaflet-control-attribution {
		display: none;
	}
	.leaflet-popup-content {
		margin: 13px 24px 13px 20px;
		line-height: 1.3;
		font-size: 13px;
		font-size: 1.08333em;
		min-height: 1px;
		font-family: Prompt, sans-serif;
	}
</style>
