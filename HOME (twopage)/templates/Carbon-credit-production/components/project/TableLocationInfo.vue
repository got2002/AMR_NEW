<template>
	<tr tabindex="0" class="focus:outline-none text-xs h-12 rounded hover:bg-theme-green-100 align-middle border border-theme-black-300">
		<td rowspan="2" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<div class="flex justify-center">
				<span class="font-medium text-sm text-theme-black-300 leading-6 uppercase mr-2">{{ locationIndex + 1 }}</span>
				<button @click="$emit('flyTo', lat,lon)">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M7.5 3.75H6A2.25 2.25 0 003.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0120.25 6v1.5m0 9V18A2.25 2.25 0 0118 20.25h-1.5m-9 0H6A2.25 2.25 0 013.75 18v-1.5M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					</svg>
				</button>
			</div>
		</td>
		<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 w-3/4 uppercase">{{lat}}</span>
		</td>
		<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 w-3/4 uppercase">{{lon}}</span>
		</td>
		<!-- <td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
			<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ feature.properties.A_NAME_T ? feature.properties.A_NAME_T + " " + feature.properties.T_NAME_T + " " + feature.properties.P_NAME_T : "-" }}</span>
		</td> -->
	</tr>
</template>

<script>
export default {
	props: ["feature", "locationIndex"],
	data() {
		return {
			lat: 0,
			lon: 0,
			first: 0,
			first2: 0,
		};
	},
	computed: {

	},
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

	},
};
</script>