from cloutron.view import *
from cloutron.plugin import *
import boto.ec2
from time import localtime, strftime


class InstanceView (TerminalView):

	@classmethod
	def configure_subparser(cls, subparsers):
		sp = subparsers.add_parser('ec2instances', help='display EC2 instances', aliases=('instances','i'))
		CloutronView.add_generic_arguments(sp)
		sp.set_defaults(func=InstanceView)
		sp.add_argument('--show-status', '-s', dest="display_status", action="store_true", help="display instance statuses (Default)", default=None)
		sp.add_argument('--hide-status', '-S', dest="display_status", action="store_false", help="do not display instance statuses")
		
	def apply_cli_config(self):
		super(InstanceView, self).apply_cli_config()
		if self.args.display_status != None:
			self.config.display_status = self.args.display_status

	def sigwinch_handler(self, sig, stack):
		self.render()
		
	def render(self):
		self.info = "EC2 Instances [%s]" % self.config.region
		self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
		self.footerleft = ""
		self.footerright = ""
		self.do_render("Loading....")
		while True:
			conn = boto.ec2.connect_to_region(self.config.region)
			res = conn.get_all_instances()
			output = self.colour("", "white", "grey", [])
			allinstances = 0
			runninginstances = 0
			for r in res:
				for inst in r.instances:
					state = ""
					pubip = ""
					privip = ""
					allinstances += 1
					if inst.state == "running":
						state = self.colour(inst.state, "green", "grey", [])
						runninginstances += 1
					elif inst.state == "stopped":
						state = self.colour(inst.state, "red", "grey", [])
					elif inst.state == "stopping":
						state = self.colour(inst.state, "red", "grey", [])
					elif inst.state == "terminating":
						state = self.colour(inst.state, "red", "grey", [])
					elif inst.state == "terminated":
						state = self.colour(inst.state, "red", "grey", [])
					elif inst.state == "shutting-down":
						state = self.colour(inst.state, "red", "grey", [])
					else:
						state = inst.state

					if inst.private_ip_address != None:
						privip = inst.private_ip_address
					if inst.ip_address != None:
						pubip = "|" + inst.ip_address

					if 'Name' in inst.tags:
						output = output + "%s (%s) [%s] %s%s\n" % (inst.tags['Name'], inst.id, state, privip, pubip)
					else:
						output = output + "%s [%s] %s%s\n" % (inst.id, state, privip, pubip)

					if self.config.display_status:
						stat = conn.get_all_instance_status(instance_ids=inst.id)
						for s in stat:
							output = output + self.colour(" \_ System Status: %s Instance Status: %s" % (str(s.system_status.status), str(s.instance_status.status)), "white", "grey", ["dark"]) + "\n"
			self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
			self.footerright = "[up:%s down:%s]" % (runninginstances, allinstances - runninginstances)
			self.do_render(output)
			if float(self.config.poll) < 30:
				time.sleep(30)
			else:
				time.sleep(float(self.config.poll))

class InstanceViewPlugin(ViewPlugin):
	plugin_type = 'view'
	name = 'instances'
	view_class = InstanceView
