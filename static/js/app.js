document.addEventListener('DOMContentLoaded', function () {

const wizardBack = document.getElementById('wizard-back');

const stepHistory = [];

function goToStep(currentStep, nextStep) {

    stepHistory.push(currentStep);

    currentStep.classList.add('hidden');
    nextStep.classList.remove('hidden');

    wizardBack.classList.remove('hidden');
    
}

wizardBack.onclick = function () {

    const previousStep = stepHistory.pop();

    if (!previousStep) return;

    document.querySelectorAll('.assessment-step')
        .forEach(step => step.classList.add('hidden'));

    previousStep.classList.remove('hidden');

    if (stepHistory.length === 0) {
        wizardBack.classList.add('hidden');
    }
};




    
    const profileStep = document.getElementById('profile-step');
    const incomeStep = document.getElementById('income-step');
    const incomeAmountStep = document.getElementById('income-amount-step');
    const expensesStep = document.getElementById('expenses-step');
    const debtStep = document.getElementById('debt-step');
    const emergencyStep = document.getElementById('emergency-step');
    const investmentStep = document.getElementById('investment-step');
    const investmentDetailsStep = document.getElementById('investment-details-step');
    const startInvestingStep = document.getElementById('start-investing-step');
    const reviewStep = document.getElementById('review-step');

    
    const incomeOptions = document.getElementById('income-options');
    const incomeAmountFields = document.getElementById('income-amount-fields');
    const debtAmountGroup = document.getElementById('debt-amount-group');



    


    
    let selectedProfile = '';
    let totalEarnedIncome = 0;

    // profile 
    const incomeMap = {
        student: ['Allowance', 'Salary', 'Other income'],
        employed: ['Salary', 'Other income'],
        selfEmployed: ['Business income', 'Other income'],
        businessOwner: ['Business income', 'Other income']
    };

    //income step
    function showIncome(profileKey) {

        incomeOptions.innerHTML = '';

        incomeMap[profileKey].forEach(function (option) {

            incomeOptions.innerHTML += `
                <label class="check-option">
                    <input type="checkbox">
                    <span>${option}</span>
                </label>
            `;
        });

       goToStep(profileStep, incomeStep);
    }

    // profile
    document.getElementById('student-btn').onclick = function () {
        selectedProfile = 'Student';
        showIncome('student');
    };

    document.getElementById('employed-btn').onclick = function () {
        selectedProfile = 'Employed';
        showIncome('employed');
    };

    document.getElementById('self-employed-btn').onclick = function () {
        selectedProfile = 'Self-employed';
        showIncome('selfEmployed');
    };

    document.getElementById('business-owner-btn').onclick = function () {
        selectedProfile = 'Business Owner';
        showIncome('businessOwner');
    };

    // Income source amount step 
    document.getElementById('income-continue').onclick = function () {

        const selected = [];

        document.querySelectorAll('#income-options input:checked')
            .forEach(function (input) {
                selected.push(input.nextElementSibling.textContent);
            });

        if (selected.length === 0) {
            alert('Please select at least one income source.');
            return;
        }

        incomeAmountFields.innerHTML = '';

        selected.forEach(function (source) {

            const fieldId = source.toLowerCase().replace(/\s+/g, '-');

            incomeAmountFields.innerHTML += `
                <div class="input-group">
                    <label for="${fieldId}">${source} amount (KSh)</label>
                    <input type="number"
                           id="${fieldId}"
                           placeholder="0"
                           min="0">
                </div>
            `;
        });

        incomeStep.classList.add('hidden');
        incomeAmountStep.classList.remove('hidden');
    };

    //  Income amounts 
    document.getElementById('income-amount-continue').onclick = function () {

        totalEarnedIncome = 0;

        document.querySelectorAll('#income-amount-fields input')
            .forEach(function (input) {
                totalEarnedIncome += Number(input.value || 0);
            });

        goToStep(incomeAmountStep, expensesStep);
    };

    //  Expenses  debt
    document.getElementById('expenses-continue').onclick = function () {

       
        goToStep(expensesStep,debtStep);

    };

    //  Debt field toggle 
    document.getElementById('debt-yes').onchange = function () {
        debtAmountGroup.classList.remove('hidden');
    };

    document.getElementById('debt-no').onchange = function () {
        debtAmountGroup.classList.add('hidden');
        document.getElementById('debt-amount').value = 0;
    };

    //  Debt  emergency savings
    document.getElementById('debt-continue').onclick = function () {

       
        goToStep(debtStep,emergencyStep);
    };

    //  Emergency  investment status 
    document.getElementById('emergency-continue').onclick = function () {

        
        goToStep(emergencyStep,investmentStep);
    };

    // Investment branching 
    document.getElementById('investment-continue').onclick = function () {

        if (document.getElementById('invest-yes').checked) {

            
            goToStep(investmentStep,investmentDetailsStep);

        } else if (document.getElementById('invest-no').checked) {

            
            goToStep(investmentStep,startInvestingStep);

        } else {

            alert('Please choose an option.');
        }
    };

    // Review 
    function showReview() {

        document.getElementById('review-profile').textContent =
            selectedProfile || '-';

        document.getElementById('review-earned').textContent =
            'KSh ' + totalEarnedIncome;

        document.getElementById('review-passive').textContent =
            'KSh ' + (document.getElementById('passive-income')?.value || 0);

        document.getElementById('review-expenses').textContent =
            'KSh ' + (document.getElementById('expenses')?.value || 0);

        document.getElementById('review-debt').textContent =
            'KSh ' + (document.getElementById('debt-amount')?.value || 0);

        document.getElementById('review-emergency').textContent =
            'KSh ' + (document.getElementById('emergency-fund')?.value || 0);

        document.getElementById('review-investing').textContent =
            document.getElementById('invest-yes').checked ? 'Yes' : 'No';
    }

    //  Investment details
    document.getElementById('investment-details-continue').onclick = function () {

       
        goToStep(investmentDetailsStep,reviewStep);
        showReview();
    };

    // Start investing
    document.getElementById('start-investing-continue').onclick = function () {

        
        goToStep(startInvestingStep,reviewStep);
        showReview();
    };

    // Final button
    document.getElementById('submit-assessment').onclick = function (e) {
        e.preventDefault();

        document.getElementById('form-earned-income').value =
            totalEarnedIncome || 0;

        document.getElementById('form-passive-income').value =
            document.getElementById('passive-income')?.value || 0;

        document.getElementById('form-expenses').value =
            document.getElementById('expenses')?.value || 0;

        document.getElementById('form-total-debts').value =
            document.getElementById('debt-amount')?.value || 0;

        document.getElementById('form-emergency-fund').value =
            document.getElementById('emergency-fund')?.value || 0;

        document.getElementById('form-dividends').value =
            document.getElementById('dividends')?.value || 0;

        const selectedRisk =
            document.querySelector('input[name="risk-preference"]:checked');

        document.getElementById('form-risk-preference').value =
            selectedRisk ? selectedRisk.value : 'low';

        

        document.getElementById('assessment-form').submit();
        };

    

});
