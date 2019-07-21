import json
from uuid import uuid4

import yaml

from config42 import ConfigManager


def args(_str):
    return _str.split(' ')


def test_help_prompt(script_runner):
    ret = script_runner.run('config42', '-h')
    ret2 = script_runner.run('config42')
    assert ret.returncode == 1
    assert ret2.returncode == 1
    # assert that config42 is the program name
    assert "usage: config42" in ret.stdout
    assert "usage: config42" in ret2.stdout


def test_literals_yaml_stdout(script_runner):
    ret = script_runner.run('config42', *args('-l key=value nested.key=value -o yaml'))
    assert ret.success

    assert "key: value" in ret.stdout
    assert "nested.key: value" in ret.stdout
    _ = yaml.load(ret.stdout, Loader=yaml.FullLoader)


def test_literals_json_stdout(script_runner):
    ret = script_runner.run('config42', *args('-l key=value nested.key=value -o json'))
    assert ret.success

    content = json.loads(ret.stdout)
    assert content.get('key') == 'value'
    assert content.get('nested.key') == 'value'


def test_literals_yaml_file(script_runner, tmp_path):
    output_yaml = str(tmp_path / "output.yaml")
    ret = script_runner.run('config42', *args('-l key=value nested.key=value -c ' + output_yaml))
    assert ret.success
    content = yaml.load(open(output_yaml))
    assert content.get('key') == 'value'
    assert content.get('nested').get('key') == 'value'


def test_literals_json_file(script_runner, tmp_path):
    output_json = str(tmp_path / "output.json")
    ret = script_runner.run('config42', *args('-l key=value nested.key=value -c ' + output_json))
    assert ret.success
    content = json.load(open(output_json))
    assert content.get('key') == 'value'
    assert content.get('nested').get('key') == 'value'


def test_literals_etcd(script_runner):
    keyspace = '/' + str(uuid4())
    ret = script_runner.run('config42', *args('-l key=value nested.key=value -c etcd --etcd-keyspace ' + keyspace))
    assert ret.success
    config_manager = ConfigManager(keyspace=keyspace)

    assert config_manager.get('key') == 'value'
    assert config_manager.get('nested').get('key') == 'value'
    assert config_manager.get('nested.key') == 'value'


def test_apply_literals(script_runner):
    keyspace = '/' + str(uuid4())
    _ = script_runner.run('config42', *args('-l key=value key2=value -c etcd --etcd-keyspace ' + keyspace))
    ret = script_runner.run('config42', *args('-a apply -l key=value2 -c etcd --etcd-keyspace ' + keyspace))
    assert ret.success
    config_manager = ConfigManager(keyspace=keyspace)
    assert config_manager.get('key') == 'value2'
    assert config_manager.get('key2') is None
    assert len(config_manager.as_dict()) == 1


def test_apply_raw(script_runner, tmp_path):
    tmp_dir = tmp_path / 'raw'
    tmp_dir.mkdir()
    path = str(tmp_dir)
    _ = script_runner.run('config42', *args('-l key=value key2=value -c raw --raw-path ' + path))
    ret = script_runner.run('config42', *args('-a apply -l key=value2 -c raw --raw-path ' + path))
    assert ret.success
    config_manager = ConfigManager(path=path)
    assert config_manager.get('key') == 'value2'
    assert config_manager.get('key') == 'value2'
    assert config_manager.get('key2') is None
    assert len(config_manager.as_dict()) == 1


def test_actions(script_runner, tmp_path):
    ret = script_runner.run('config42', *args('-l key=value -o json'))
    assert ret.success
    ret = script_runner.run('config42', *args('-a apply -l key=value -o json'))
    assert not ret.success
    ret = script_runner.run('config42', *args('-a destroy -l key=value -o json'))
    assert not ret.success
    ret = script_runner.run('config42', *args('-a merge -l key=value -o json'))
    assert not ret.success
    file = str(tmp_path / "output.json")
    ret = script_runner.run('config42', *args('-a merge -l key=value -c ' + file))
    assert ret.success
    ret = script_runner.run('config42', *args('-a apply -l key=value -c ' + file))
    assert ret.success
    ret = script_runner.run('config42', *args('-a destroy -l key=value -c ' + file))
    assert ret.success
    ret = script_runner.run('config42', *args('-a read -l key=value -c ' + file))
    assert ret.success


def test_logging_to_stderr(script_runner):
    keyspace = '/' + str(uuid4())
    ret = script_runner.run('config42', *args('-l key=value key2=value -c etcd --etcd-keyspace ' + keyspace))
    assert len(ret.stderr) == 0  # No log
    ret = script_runner.run('config42', *args('-l key=value key2=value -c etcd --etcd-keyspace -v' + keyspace))
    assert len(ret.stderr)  # with log
