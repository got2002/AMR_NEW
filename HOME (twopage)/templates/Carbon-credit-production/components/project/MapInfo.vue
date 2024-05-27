<template>
	<div>
		<div :id="'map-' + form._id" :style="{ width: width + widthUnit, height: height + heightUnit }" class="z-10 border border-carbon-sorf-dark"></div>
		<div @click="addressExpand = !addressExpand" class="bg-gray-300 bg-opacity-50 p-4 flex gap-3 mt-3 justify-between w-full shadow cursor-pointer">
			<label>{{$t('project.view_page.adress_position_title',{amount:form.location.features.length})}}</label>
			<svg v-if="!addressExpand" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
			</svg>
			<svg v-if="addressExpand" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
			</svg>
		</div>
		<div v-if="addressExpand" class="w-full bg-gray-50 p-2">
			<div class="w-full grid grid-cols-1 xl:grid-cols-1 overflow-x-auto">
				<table class="items-center w-full space-y-6 border border-theme-black-300">
					<thead>
						<tr>
							<template v-for="(item, idx) in table.head">
								<ApiHeadSlotWhite :text="item.name" :key="idx" :align="item.align" />
							</template>
						</tr>
					</thead>
					<tbody class="bg-white border border-theme-black-300">
						<template v-for="(data, index) in form.location.features">
							<ProjectTableLocationInfo :feature="data" :locationIndex="index" @flyTo="flyTo" :key="index" />
							<tr v-if="form.address[index] != undefined && $i18n.locale === 'th'" :key="index + '-div'">
								<td colspan="4">
									<div class="grid grid-cols-6">
										<div class="col-span-2 flex items-center justify-center border-2 bg-gray-200 text-sm">{{ $t("project.create_page.address.subtitle") }}</div>
										<span type="text" class="col-span-4 px-3 py-2 text-center border-2 text-sm">{{ form.address[index] }}</span>
									</div>
								</td>
							</tr>
							<tr v-else :key="index + '-div_en'">
								<td colspan="4">
									<div class="grid grid-cols-6">
										<div class="col-span-2 flex items-center justify-center border-2 bg-gray-200 text-sm">{{ $t("project.create_page.address.subtitle") }}</div>
										<span type="text" class="col-span-4 px-3 py-2 text-center border-2 text-sm">{{ form.address_en[index] }}</span>
									</div>
								</td>
							</tr>
						</template>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["form", "width", "widthUnit", "height", "heightUnit"],
		data() {
			return {
				map: null,
				marker: null,
				addressExpand: false,
				table: {
					head: [
						{
							name: this.$t("project.table.header.no"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("project.table.header.lat"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("project.table.header.lon"),
							align: "center",
							filterable: false,
						},
						// {
						// 	name: this.$t("project.table.header.location"),
						// 	align: "center",
						// 	filterable: false,
						// },
					],
				},
			};
		},
		mounted() {
			// console.log(this.strip);
			const L = window.L;
			this.map = L.map("map-" + this.form._id, { zoomControl: false });

			L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(this.map);
			const osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
			var gUrl = "http://mt0.google.com/vt/lyrs=s&x={x}&y={y}&z={z}";
			var gAttribution = "google";
			var googlesat = new L.TileLayer(gUrl, { maxZoom: 18, attribution: gAttribution });
			const baseMaps = {
				OpenStreetMap: osm,
				GoogleSat: googlesat,
			};
			const overlays = {};
			this.marker = new L.FeatureGroup().addTo(this.map);
			L.control.layers(baseMaps, overlays, { position: "topright" }).addTo(this.map);
			if (this.form.location !== null) {
				let count = 1;
				this.form.location.features.forEach((element) => {
					let blackIcon = new L.Icon({
						iconUrl: "https://raw.githubusercontent.com/sheiun/leaflet-color-number-markers/main/dist/img/blue/marker-icon-2x-blue-" + `${count}` + ".png",
						shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
						iconSize: [25, 41],
						iconAnchor: [12, 41],
						popupAnchor: [1, -34],
						shadowSize: [41, 41],
					});
					const requestPolygon = element;
					let latlon = [];
					latlon[1] = parseFloat(element.geometry.coordinates[0]).toFixed(6);
					latlon[0] = parseFloat(element.geometry.coordinates[1]).toFixed(6);
					const myLayer = L.marker(latlon, { icon: blackIcon }).addTo(this.map);
					// this.map.flyTo(latlon, 14, { animate: false });
					this.marker.addLayer(myLayer);
					this.map.fitBounds(this.marker.getBounds());
					count++;
				});
			}
		},
		methods: {
			flyTo(lat, lon) {
				this.map.flyTo([lat, lon], 14, { animate: false });
				const elmntToView = document.getElementById("map-" + this.form._id);
				elmntToView.scrollIntoView({behavior: "smooth"});
			},
		},
	};
</script>

<style>
	.leaflet-control-attribution {
		display: none;
	}
</style>
