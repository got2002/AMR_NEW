
<template>
	<div>
		<div class="container mx-auto my-5 p-5">
			<div class="md:flex no-wrap md:-mx-2">
				<!-- Left Side -->
				<div class="w-full md:w-3/12 md:mx-2">
					<!-- Profile Card -->
					<div class="bg-white p-3 border-t-4 border-green-400">
						<div class="image overflow-hidden">
							<img class="h-auto w-full mx-auto" :src="'' + form.faceIdImage" alt="" />
						</div>
						<h1 class="text-gray-900 font-bold text-xl leading-8 my-1">{{fullname(form)}}</h1>
					</div>
				</div>
				<!-- Right Side -->
				<div class="w-full md:w-9/12 mx-2 h-64">
					<!-- Profile tab -->
					<!-- About Section -->
					<div class="bg-white p-3 shadow-sm rounded-sm">
						<div class="flex items-center space-x-2 font-semibold text-gray-900 leading-8">
							<span clas="text-green-500">
								<svg class="h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
								</svg>
							</span>
							<span class="tracking-wide">About</span>
						</div>
						<div class="text-gray-700">
							<div class="grid md:grid-cols-2 text-sm">
								<div class="grid grid-cols-2">
									<div class="px-4 py-2 font-semibold">First Name</div>
									<div class="px-4 py-2">{{form.firstname}}</div>
								</div>
								<div class="grid grid-cols-2">
									<div class="px-4 py-2 font-semibold">Last Name</div>
									<div class="px-4 py-2">{{form.lastname}}</div>
								</div>
								<div class="grid grid-cols-2">
									<div class="px-4 py-2 font-semibold">Contact No.</div>
									<div class="px-4 py-2">{{form.phoneNumber}}</div>
								</div>
								<div class="grid grid-cols-2">
									<div class="px-4 py-2 font-semibold">Email.</div>
									<div class="px-4 py-2">
										<a class="text-blue-800" href="mailto:jane@example.com">{{form.email}}</a>
									</div>
								</div>
							</div>
						</div>
					</div>
					<!-- End of about section -->
				</div>
			</div>
		</div>
	</div>
</template>
<script>
export default {
	props: ["form"],
	name: "UserInfoform",
	middleware: ["auth"],
	components: {},
	computed: {},
	data() {
		return {
			dropdown: {
				users: [],
				provinces: [],
				districts: [],
				subDistricts: [],
			},
			isData: false,
		};
	},
	watch: {
	},
	async mounted() {},
	methods: {
        fullname(data) {
			return data.firstname + " " + data.lastname;
		},
	},
};
</script>