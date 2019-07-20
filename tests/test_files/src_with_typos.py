
def start_ad_company(company) -> bool:
    """Созадет ркеламную кампанию."""
    if company.owner.total_budget < company.budget:
        company.owner.send_message('Для содание рекламной компании недостаточно бджета')
        return False
