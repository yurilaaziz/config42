from config42 import ConfigManager


def test_render_template(sample_config):
    config_manager = ConfigManager()
    config_manager.set_many(sample_config)
    config_manager.set('template', 'nested = {{simple_dict.key}}')
    assert "" == config_manager.render("{{nothing}}")
    assert "default_value" == config_manager.render("{{nothing | default('default_value')}}")
    assert 'value' == config_manager.render('{{simple}}')
    assert 'value' == config_manager.render('{{simple_dict.key}}')
    assert 'nested = value' == config_manager.render('{{template}}')


def test_get_template(sample_config):
    config_manager = ConfigManager()
    config_manager.set_many(sample_config)
    config_manager.set('template', 'nested = {{simple_dict.key}}')
    config_manager.set('nested_template', 'nested = {{template}}')
    config_manager.set('recursive', 'nested = {{recursive}}')
    assert 'nested = value' == config_manager.get('template')
    assert 'nested = nested = value' == config_manager.get('nested_template')
    assert config_manager.get('recursive') is None
    assert config_manager.get('not_key') is None
