<template>
	<div>
		<div class="relative">
			<!-- <div class="grid grid-cols-1 md:grid-cols-2 gap-4 absolute z-50 bottom-0 m-4 bg-white p-2 rounded-sm">
				<div>
					<label class="text-gray-600 font-medium text-sm">{{ $t("project.view_page.latitude") }}</label>
					<div>
						<input v-model.number="lat" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" required />
					</div>
				</div>
				<div>
					<label class="text-gray-600 font-medium text-sm">{{ $t("project.view_page.longitude") }}</label>
					<div>
						<input v-model.number="lon" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" required />
					</div>
				</div>
			</div> -->
			<div id="map-create" :style="{ width: width + widthUnit, height: height + heightUnit }" class="z-10 border border-carbon-sorf-dark"></div>
		</div>
		<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 mt-4 overflow-x-auto">
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
						<ProjectTableLocation :feature="data" :form="form" :locationIndex="index" @updateFeature="updateFeature" @deleteFeature="deleteFeature" @flyTo="flyTo" :selected="select" :ref="'TableLocation' + index" :key="'TableLocation' + index" />
						<tr :key="'address-thai' + index">
							<td colspan="2">
								<div class="flex items-center">
									<label class="w-48 px-3 py-2 text-center border-2 bg-gray-200 text-sm">{{ $t("project.create_page.address.subtitle_lang.th") }}</label>
									<input v-model="form.address[index]" type="text" class="w-full px-3 py-2 text-center border-2 text-sm"/>
								</div>
								<span class="text-left text-red-500 text-sm" v-if="!$v.form.address.$each[index].required && isSubmitted">{{ $t("project.create_page.form_validation.address") }}</span>
							</td>
						</tr>
						<tr :key="'address-eng' + index">
							<td colspan="2">
								<div class="flex items-center">
									<label class="w-48 px-3 py-2 text-center border-2 bg-gray-200 text-sm">{{ $t("project.create_page.address.subtitle_lang.en") }}</label>
									<input v-model="form.address_en[index]" type="text" class="w-full px-3 py-2 text-center border-2 text-sm" />
								</div>
								<span class="text-left text-red-500 text-sm" v-if="!$v.form.address_en.$each[index].required && isSubmitted">{{ $t("project.create_page.form_validation.address") }}</span>
							</td>
						</tr>
					</template>
				</tbody>
			</table>
			<div class="flex items-center gap-2 text-white justify-center py-3">
				<button @click="addLocation()" class="w-1/3 py-3 text-center bg-green-500 cursor-pointer">{{ $t("button.add") }}</button>
			</div>
		</div>
	</div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
export default {
	props: ["form", "width", "widthUnit", "height", "heightUnit","isSubmitted"],
	validations() {
		return {
			form: {
				address: {
					$each: { required },
				},
				address_en: {
					$each: { required },
				},
			},
		};
	},
	data() {
		return {
			previewLayer: null,
			select: null,
			first: true,
			map: null,
			marker: null,
			lat: null,
			lon: null,
			markers: [],
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
					{
						name: "",
						align: "center",
						filterable: false,
					},
				],
			},
		};
	},
	watch: {},
	mounted() {
		// console.log(this.strip);
		const L = window.L;
		this.map = L.map("map-create", { zoomControl: false }).setView([13, 100], 6);

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
				this.markers.push(myLayer);
				this.map.fitBounds(this.marker.getBounds());
				count++;
			});
		}

		let app = this;
		this.map.on(L.Draw.Event.CREATED, function (e) {
			var layer = e.layer;
			const lat = layer._latlng.lat.toFixed(6);
			const lon = layer._latlng.lng.toFixed(6);
			app.form.location.features[app.select].geometry.coordinates[1] = parseFloat(lat);
			app.form.location.features[app.select].geometry.coordinates[0] = parseFloat(lon);
			const latlon = L.latLng(parseFloat(lat), parseFloat(lon));
			app.markers[app.select].setLatLng(latlon);
			app.$refs["TableLocation" + app.select][0].updateLocation();
		});
	},
	methods: {
		flyTo(lat, lon, index) {
			const L = window.L;
			this.select = index;
			if (this.first) {
				let options = {
					draw: {
						polyline: false,
						marker: true,
						circlemarker: false,
						circle: false,
						polygon: false,
						rectangle: false,
					},
				};
				const drawControl = new L.Control.Draw(options);
				this.map.addControl(drawControl);
				this.first = false;
			}
			this.map.flyTo([lat, lon], 14, { animate: false });
		},
		updateFeature(value) {
			console.log(value);
			const L = window.L;
			const lat = value[0];
			const lon = value[1];
			const locationIndex = value[2];
			this.form.location.features[locationIndex].geometry.coordinates[1] = lat;
			this.form.location.features[locationIndex].geometry.coordinates[0] = lon;
			const latlon = L.latLng(lat, lon);
			this.markers[locationIndex].setLatLng(latlon);
			this.map.flyTo([lat, lon], 14, { animate: false });
		},
		addLocation() {
			let location = {
				geometry: {
					coordinates: [100, 13],
					type: "Point",
				},
				properties: {},
				type: "Feature",
			};
			this.form.location.features.push(location);
			this.form.address.push("");
			this.form.address_en.push("");
			this.createMarker(13, 100);
		},
		deleteFeature(index) {
			const L = window.L;
			this.form.location.features.splice(index, 1);
			this.form.address.splice(index, 1);
			this.form.address_en.splice(index, 1);
			this.marker.removeLayer(this.markers[index]);
			this.markers.splice(index, 1);
			let count = 1;
			this.marker.eachLayer(function (layer) {
				let blackIcon = new L.Icon({
					iconUrl: "https://raw.githubusercontent.com/sheiun/leaflet-color-number-markers/main/dist/img/blue/marker-icon-2x-blue-" + `${count}` + ".png",
					shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
					iconSize: [25, 41],
					iconAnchor: [12, 41],
					popupAnchor: [1, -34],
					shadowSize: [41, 41],
				});
				layer.setIcon(blackIcon);
				count++;
			});
			console.log(this.form.location.features);
			// const backup = this.form.location.features
			// this.form.location.features = []
			// this.form.location.features = backup
		},
		createMarker(lat, lon) {
			const L = window.L;
			const count = this.form.location.features.length;
			let blackIcon = new L.Icon({
				iconUrl: "https://raw.githubusercontent.com/sheiun/leaflet-color-number-markers/main/dist/img/blue/marker-icon-2x-blue-" + `${count}` + ".png",
				shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
				iconSize: [25, 41],
				iconAnchor: [12, 41],
				popupAnchor: [1, -34],
				shadowSize: [41, 41],
			});
			const myLayer = L.marker([lat, lon], { icon: blackIcon }).addTo(this.map);
			// this.map.flyTo([lat, lon], 14, { animate: false });
			this.marker.addLayer(myLayer);
			this.markers.push(myLayer);
			this.map.fitBounds(this.marker.getBounds());
		},
	},
};
</script>

<style>
.leaflet-control-attribution {
	display: none;
}
</style>