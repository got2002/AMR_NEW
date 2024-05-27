export default function ({ store, redirect }) {
  // If the user is not authenticated
  if (!store.state.auth.loggedIn || (store.state.auth.loggedIn && store.state.auth.user.role !== 99)) {
    return redirect('/')
  }
}
