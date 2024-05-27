<template>
	<div class="modal-overlay">
		<div class="modal">
			<ProjectTablePDF2 :number="number" :form="form" :edit="edit"/>
		</div>
		<div class="close" @click="$emit('close-modal')">
			<div class="bg-theme-green-200 rounded">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</div>
		</div>
	</div>
</template>
  
  <script>
export default {
    props:['number','form','edit'],
    data() {
        return {};
    },
};
</script>
  <style scoped>
.modal-overlay {
    z-index: 99999999;
	position: fixed;
	top: 0;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	justify-content: center;
	background-color: #626262da;
}

.modal {
	text-align: center;
	background-color: white;
	height: auto;
	width: auto;
	min-width: 500px;
	margin-top: 10%;
	padding: 10px 20px;
	border-radius: 20px;
}
.close {
	margin: 10% 0 0 16px;
	cursor: pointer;
}

.close-img {
	width: 25px;
}

.check {
	width: 150px;
}

h6 {
	font-weight: 500;
	font-size: 28px;
	margin: 20px 0;
}

p {
	font-size: 16px;
	margin: 20px 0;
}
</style>