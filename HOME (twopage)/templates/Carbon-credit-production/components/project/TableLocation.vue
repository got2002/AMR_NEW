<template>
	<tr tabindex="0" @click="$emit('flyTo', lat, lon, locationIndex)" class="focus:outline-none text-xs h-12 rounded align-middle border border-theme-black-300" :class="{ 'bg-theme-green-100': selected == locationIndex, 'hover:bg-theme-green-100': selected != locationIndex }">
		<td rowspan="3" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<div class="flex justify-center">
				<span class="font-medium text-sm text-theme-black-300 leading-6 uppercase mr-2">{{ locationIndex + 1 }}</span>
				<!-- <button @click="$emit('flyTo', lat, lon)">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M7.5 3.75H6A2.25 2.25 0 003.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0120.25 6v1.5m0 9V18A2.25 2.25 0 0118 20.25h-1.5m-9 0H6A2.25 2.25 0 013.75 18v-1.5M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					</svg>
				</button> -->
				<!-- <div class="flex items-center">
					<input id="default-radio-1" type="radio" :value="locationIndex" @change="$emit('flyTo', lat, lon,locationIndex)" name="default-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500">
				</div> -->
			</div>
		</td>
		<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<input type="number" step="any" class="font-medium text-sm text-theme-black-300 leading-6 ml-2 w-3/4 uppercase border bg-gray-50 text-center" v-model.number="lat" />
		</td>
		<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<input type="number" step="any" class="font-medium text-sm text-theme-black-300 leading-6 ml-2 w-3/4 uppercase border bg-gray-50 text-center" v-model.number="lon" />
		</td>
		<!-- <td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ feature.properties.A_NAME_T ? feature.properties.A_NAME_T + " " + feature.properties.T_NAME_T + " " + feature.properties.P_NAME_T : "-" }}</span>
		</td> -->
		<td rowspan="3" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<div class="flex justify-center">
				<button @click="deleteLocation(locationIndex)" target="_blank" class="">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
					</svg>
				</button>
			</div>
		</td>
		<!-- <td>
			<label class="w-32 px-3 py-2 text-center border-2 bg-gray-200">{{ $t("project.create_page.address.subtitle") }} ({{ locationIndex + 1 }})</label>
			<input v-model="form.address[locationIndex]" type="text" class="w-full px-3 py-2 text-center border-2" />
		</td> -->
	</tr>
</template>

<script>
export default {
	props: ["feature", "locationIndex", "selected", "form"],
	data() {
		return {
			lat: 0,
			lon: 0,
			first: 0,
			first2: 0,
		};
	},
	computed: {},
	watch: {
		lat: function () {
			if (this.first !== 0) {
				this.$emit("updateFeature", [this.lat, this.lon, this.locationIndex]);
			}
			this.first = 1;
		},
		lon: function (val, newValue) {
			// const L = window.L;
			// this.form.location.geometry.coordinates[1] = this.lat;
			// this.form.location.geometry.coordinates[0] = this.lon;
			// this.marker.clearLayers().addLayer(L.marker([this.lat, this.lon]));
			// this.map.setView(new L.latLng(this.lat, this.lon));
			if (this.first2 !== 0) {
				this.$emit("updateFeature", [this.lat, this.lon, this.locationIndex]);
			}
			this.first2 = 1;
		},
	},
	mounted() {
		this.lat = this.feature.geometry.coordinates[1];
		this.lon = this.feature.geometry.coordinates[0];
	},
	updated() {
		this.lat = this.feature.geometry.coordinates[1];
		this.lon = this.feature.geometry.coordinates[0];
	},
	methods: {
		updateLocation() {
			this.lat = this.feature.geometry.coordinates[1];
			this.lon = this.feature.geometry.coordinates[0];
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
		},
		deleteLocation(index) {
			this.$emit("deleteFeature", index);
		},
		seePdf(value) {
			console.log(value);
			this.dataModal = value;
			this.showModal = true;
		},
		dateToString(date) {
			const result = new Date(date).toLocaleDateString("th-TH", {
				year: "numeric",
				month: "long",
				day: "numeric",
			});
			return result;
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
		sumCarbon() {
			let sum = 0;
			// console.log(this.form);
			this.form.carbon_credit_cert.forEach((element) => {
				sum += element.amount;
			});
			return sum.toLocaleString();
		},
	},
};
</script>