

function deleteExpense(expenseId) {
  fetch("/delete-expense", {
    method: "POST",
    body: JSON.stringify({ entryId: expenseId }),
  }).then((_res) => {
    window.location.reload();
  });
}

function deleteIncome(incomeId) {
  fetch("/delete-income", {
    method: "POST",
    body: JSON.stringify({ entryId: incomeId }),
  }).then((_res) => {
    window.location.reload();
  });
}

function editExpense(expenseId, data) {
  fetch(`/edit-expense/${expenseId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data),
  }).then((_res) => {
    window.location.reload();
  });
}

function editIncome(incomeId, data) {
  fetch(`/edit-income/${incomeId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data),
  }).then((_res) => {
    window.location.reload();
  });
}

document.querySelectorAll(".edit-expense-button").forEach(function (button) {
  button.addEventListener("click", function () {
    var expenseId = this.getAttribute("data-expense-id");
    window.location.href = "/edit-expense/" + expenseId;
  });
});

document.querySelectorAll(".edit-income-button").forEach(function (button) {
  button.addEventListener("click", function () {
    var incomeId = this.getAttribute("data-income-id");
    window.location.href = "/edit-income/" + incomeId;
  });
});