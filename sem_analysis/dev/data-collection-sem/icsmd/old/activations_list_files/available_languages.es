










AUI.add(
	'portal-available-languages',
	function(A) {
		var available = {};

		var direction = {};

		

			available['en_US'] = 'English (United States)';
			direction['en_US'] = 'ltr';

		

			available['es_ES'] = 'Spanish (Spain)';
			direction['es_ES'] = 'ltr';

		

			available['fr_FR'] = 'French (France)';
			direction['fr_FR'] = 'ltr';

		

			available['ja_JP'] = 'Japanese (Japan)';
			direction['ja_JP'] = 'ltr';

		

			available['zh_CN'] = 'Chinese (China)';
			direction['zh_CN'] = 'ltr';

		

			available['ru_RU'] = 'Russian (Russia)';
			direction['ru_RU'] = 'ltr';

		

			available['ko_KR'] = 'Korean (South Korea)';
			direction['ko_KR'] = 'ltr';

		

			available['pt_BR'] = 'Portuguese (Brazil)';
			direction['pt_BR'] = 'ltr';

		

		Liferay.Language.available = available;
		Liferay.Language.direction = direction;
	},
	'',
	{
		requires: ['liferay-language']
	}
);