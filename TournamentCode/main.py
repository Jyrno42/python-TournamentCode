import json
import argparse

import TournamentCode


class TournamentCodeCreator(object):
    """ A simple commandline tool for creating
        TournamentCodes using the provided library.
    """

    def run(self):
        parser = argparse.ArgumentParser(description='TournamentCode Creator Tool')

        parser.add_argument('-c', action='store_true', help='Use commandline mode.')
        parser.add_argument('--team_size', type=int, help='The team size you want')
        parser.add_argument('--map', type=int, help='The map', choices=dict(TournamentCode.TournamentCode.MAPS).keys())
        parser.add_argument('--gm', type=int, help='The game mode', choices=dict(TournamentCode.TournamentCode.PICK_MODES).keys())
        parser.add_argument('--spec', help='spectating rule', choices=dict(TournamentCode.TournamentCode.SPEC_CONFIG).keys())

        parser.add_argument('--name', help='Game name')
        parser.add_argument('--password', help='Game password')
        parser.add_argument('--report_url', help='Reportback url', default='http://example.com/report')
        parser.add_argument('--extra_data', help='Passback data packet', default='example')

        args = parser.parse_args()

        if args.c:
            try:
                config = TournamentCode.GameConfig('example_game')
                config.set_config_value('name', args.name)
                config.set_config_value('password', args.password)
                config.set_config_value('report_url', args.report_url)
                config.set_config_value('extra_data', args.extra_data)

                result = TournamentCode.TournamentCode.generate(config=config, map_id=args.map, pick_mode=args.gm,
                                                                team_size=args.team_size, spec_config=args.spec)

                print(result)

            except TournamentCode.TournamentCodeException as e:
                print('TournamentCode ERROR: %s' % e.message)
                return 2

            except Exception as e:
                print('General ERROR: %s' % e.message)
                return 1

            else:
                return 0

        else:
            return self.run_interactive()

    def run_interactive(self):
        """ Create a TournamentCode using a wizard like approach.
        """
        print('TournamentCode Creator Tool')
        print('='*40)
        print(' ')

        print('Doing configuration (Note: Enter None to set an empty value, when pressing enter we use the default)')
        print('-'*40)

        config = TournamentCode.GameConfig('example_game')
        self.interactive_config(config, ['name', 'password', 'report_url', 'extra_data'])

        print(' ')
        print('Game configuration Done')
        print(' ')

        the_map = self.menu_question('Select Map', dict(TournamentCode.TournamentCode.MAPS))
        pick_mode = self.menu_question('Select Game Mode', dict(TournamentCode.TournamentCode.PICK_MODES))
        spec_conf = self.menu_question('Spectating', dict(TournamentCode.TournamentCode.SPEC_CONFIG), is_int=False)

        team_size = self.menu_question('Team size', dict([(x, x) for x in
                                                          range(0, 3 if the_map == TournamentCode.TournamentCode.TWISTED_TREELINE else 5)]))

        print(' ')
        print('Game info: ')
        print('-'*40)

        print('Name:          %s' % config.name)
        print('Password:      %s' % config.password)
        print('Report url:    %s' % config.report_url)
        print('Extra data:    %s' % json.dumps(config.extra_data))
        print(' ')
        print('Map:           %s' % dict(TournamentCode.TournamentCode.MAPS)[the_map])
        print('Game Mode:     %s' % dict(TournamentCode.TournamentCode.PICK_MODES)[pick_mode])
        print('Spectators:    %s' % dict(TournamentCode.TournamentCode.SPEC_CONFIG)[spec_conf])
        print('Team size:     %s' % team_size)
        print(' ')

        print('TournamentCode: ')
        print('-'*40)
        print(' ')

        print(TournamentCode.TournamentCode.generate(config=config, map_id=the_map, pick_mode=pick_mode,
                                                     team_size=team_size, spec_config=spec_conf))

        print(' ')

        return 0

    @staticmethod
    def menu_question(label, options, is_int=True):
        print(label)
        print('-'*40)
        for opt in sorted(options.keys()):
            print('    %s - %s' % (opt, options[opt]))
        print('-'*40)
        print(' ')

        while True:
            value = raw_input('>>> ')
            try:
                if is_int:
                    value = int(value)

                if value in options.keys():
                    print('Selected %s' % options[value])
                    print(' ')

                    return value
            except ValueError:
                pass

            print('Try again...')

        return None

    @staticmethod
    def interactive_config(obj, attrs):
        for attr in attrs:
            while True:
                cur_value = getattr(obj, attr, None)
                result = raw_input('Enter game %s%s: ' % (attr, ' [%s]' % cur_value if cur_value is not None else ''))

                if result == 'None':
                    result = None

                elif not result:
                    # Break out of inner loop...
                    break

                try:
                    obj.set_config_value(attr, result)
                    break

                except TournamentCode.TournamentCodeException as e:
                    print('ERROR: %s' % e.message)
                    continue

if __name__ == '__main__':
    TournamentCodeCreator().run()
