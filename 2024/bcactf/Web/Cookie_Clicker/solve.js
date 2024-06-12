// Put in console
socket.off('error');
socket.emit('click', JSON.stringify({"power": 1e50, "value": send.value}));
socket.emit('click', JSON.stringify({"power": 5, "value": send.value}));

// bcactf{H0w_Did_Y0u_Cl1ck_S0_M4ny_T1mes_123}
